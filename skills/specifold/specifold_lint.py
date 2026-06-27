#!/usr/bin/env python3
"""Specifold reference linter — enforces the integrity rules from SPEC.md.

The format already *specifies* these rules (see the rule table in SPEC.md); this
makes them executable so a spec can be checked rather than eyeballed. Structural
only: it says the graph hangs together, not that the architecture is good.

    python3 specifold_lint.py [spec-dir]      # defaults to the current directory

Exit code is non-zero if any `error`-level rule fails. `warn` never fails the run.
Rule ids match SPEC.md so the linter and any hosted store enforce the same thing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

UNDERSTOOD_FORMATS = {"0.1", "0.2"}  # v0.1 specs remain valid under a v0.2 tool


class Node:
    def __init__(self, fm: dict, body: str, source: str | None = None):
        self.source = source  # a path or label for diagnostics; not read by any rule
        self.fm = fm
        self.body = body
        self.id = fm.get("id")
        self.kind = fm.get("kind")
        self.parent = fm.get("parent")  # may be the literal None (root) or absent

    def sections(self) -> dict[str, str]:
        """Map `## Heading` -> the text beneath it (until the next `##`)."""
        out, cur, buf = {}, None, []
        for line in self.body.splitlines():
            m = re.match(r"^##\s+(.*\S)\s*$", line)
            if m:
                if cur is not None:
                    out[cur] = "\n".join(buf).strip()
                cur, buf = m.group(1).strip(), []
            elif cur is not None:
                buf.append(line)
        if cur is not None:
            out[cur] = "\n".join(buf).strip()
        return out


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm = yaml.safe_load(parts[1]) or {}
    return (fm if isinstance(fm, dict) else {}), parts[2]


def parse_node(text: str, source: str | None = None) -> "Node | None":
    """Build a Node from one node file's text, or None if it isn't a spec node.

    A spec node is any markdown with frontmatter carrying an `id`; anything else
    (plain prose, the format's own docs) returns None. v0.1 nodes have no `kind`, so
    it defaults to `component` (only components existed then). This is the in-memory
    entry the hosted store uses — it never touches the filesystem."""
    fm, body = _split_frontmatter(text)
    if not fm or "id" not in fm:
        return None
    fm.setdefault("kind", "component")
    return Node(fm, body, source)


def parse_manifest(text: str) -> dict:
    """Parse a specifold.yaml manifest into a dict (empty dict if blank/non-mapping)."""
    data = yaml.safe_load(text) or {}
    return data if isinstance(data, dict) else {}


def _edge_target(e) -> str | None:
    if isinstance(e, str):
        return e
    if isinstance(e, dict):
        return e.get("to")
    return None


def _is_one_sentence(s: str) -> bool:
    s = (s or "").strip()
    if not s:
        return False
    # split on sentence-enders followed by space; >1 non-empty piece => multi-sentence
    pieces = [p for p in re.split(r"[.!?]+\s+", s) if p.strip()]
    return len(pieces) <= 1


class Report:
    def __init__(self):
        self.results: list[tuple[str, str, list[str]]] = []  # (rule, sev, failures)

    def rule(self, rule_id: str, sev: str, failures: list[str]):
        self.results.append((rule_id, sev, failures))

    def has_errors(self) -> bool:
        """True if any error-level rule failed — the gate a hosted write checks."""
        return any(sev == "error" and failures for _, sev, failures in self.results)

    def summary(self) -> dict:
        """Structured view for programmatic callers (the service): failing rules
        grouped by severity. An empty `errors` list means the write may be admitted."""
        return {
            "errors": [
                {"rule": r, "failures": f} for r, sev, f in self.results if sev == "error" and f
            ],
            "warnings": [
                {"rule": r, "failures": f} for r, sev, f in self.results if sev == "warn" and f
            ],
        }

    def render_and_exit(self):
        errors = warns = 0
        width = max((len(r) for r, _, _ in self.results), default=0)
        for rule_id, sev, failures in self.results:
            if failures:
                mark = "✗"
                (errors := errors + 1) if sev == "error" else (warns := warns + 1)
            else:
                mark = "✓"
            print(f"  {mark} {rule_id:<{width}}  {sev}")
            for f in failures:
                print(f"        - {f}")
        print()
        if errors:
            print(f"FAIL — {errors} error(s), {warns} warning(s)")
            sys.exit(1)
        print(f"OK — 0 errors, {warns} warning(s)")
        sys.exit(0)


def load_spec(spec_dir: Path):
    """Filesystem adapter: read a spec directory into (manifest paths, nodes).

    The only filesystem-aware part of the linter; the rules themselves run over the
    in-memory nodes via `lint_nodes`."""
    manifests = sorted(spec_dir.rglob("specifold.yaml"))
    nodes: list[Node] = []
    for md in sorted(spec_dir.rglob("*.md")):
        if md.name.upper() in {"README.MD", "SPEC.MD", "SKILL.MD", "GLOSSARY.MD"}:
            continue
        node = parse_node(md.read_text(encoding="utf-8"), source=str(md))
        if node is not None:
            nodes.append(node)
    return manifests, nodes


def lint(spec_dir: Path) -> Report:
    """Filesystem entry (the CLI path): load a spec dir, then lint it in memory."""
    manifests, nodes = load_spec(spec_dir)
    rel = lambda p: str(p.relative_to(spec_dir))  # noqa: E731
    manifest_problems: list[str] = []
    manifest = None
    if not manifests:
        manifest_problems.append("no specifold.yaml found in the spec")
    elif len(manifests) > 1:
        manifest_problems.append(
            "more than one specifold.yaml (a spec has exactly one root manifest): "
            + ", ".join(rel(m) for m in manifests)
        )
    else:
        manifest = parse_manifest(manifests[0].read_text(encoding="utf-8"))
    return lint_nodes(nodes, manifest, manifest_problems=manifest_problems)


def lint_nodes(nodes, manifest, *, manifest_problems=()) -> Report:
    """Lint an in-memory spec: the node list plus the single manifest dict (or None).

    The pure rule engine — no filesystem, no model — shared by the CLI and the hosted
    store, so a consistency rule is enforced identically wherever a spec is drafted.
    `manifest_problems` carries manifest-cardinality failures the in-memory caller can't
    see for itself: the service holds exactly one manifest and passes none, while the
    filesystem loader passes 'no manifest' / 'more than one' here."""
    rep = Report()

    # spec/declared-format — manifest present, singular, and format understood
    fmt_failures = list(manifest_problems)
    if manifest is not None and manifest.get("spec_format") not in UNDERSTOOD_FORMATS:
        fmt_failures.append(f"spec_format {manifest.get('spec_format')!r} not understood")
    rep.rule("spec/declared-format", "error", fmt_failures)

    components = [n for n in nodes if n.kind == "component"]
    features = [n for n in nodes if n.kind == "feature"]
    by_id = {n.id: n for n in nodes}

    # spec/unique-ids
    seen, dupes = set(), set()
    for n in nodes:
        (dupes.add(n.id) if n.id in seen else seen.add(n.id))
    rep.rule("spec/unique-ids", "error", [f"duplicate id: {d}" for d in sorted(dupes)])

    # spec/single-root — exactly one component with parent: null, named by manifest.root
    roots = [n for n in components if n.parent is None]
    sr = []
    if len(roots) != 1:
        sr.append(f"expected exactly one root component (parent: null), found {len(roots)}: "
                  + ", ".join(sorted(r.id for r in roots)))
    elif manifest is not None and manifest.get("root") != roots[0].id:
        sr.append(f"manifest root {manifest.get('root')!r} does not name the root component {roots[0].id!r}")
    rep.rule("spec/single-root", "error", sr)

    # spec/parent-exists
    pe = [f"{n.id}: parent {n.parent!r} does not exist"
          for n in nodes if n.parent is not None and n.parent not in by_id]
    rep.rule("spec/parent-exists", "error", pe)

    # spec/parent-same-kind
    psk = [f"{n.id} ({n.kind}) → parent {n.parent} ({by_id[n.parent].kind})"
           for n in nodes if n.parent in by_id and by_id[n.parent].kind != n.kind]
    rep.rule("spec/parent-same-kind", "error", psk)

    # spec/component-tree-acyclic — tree + every component reachable from the root
    cta = []
    comp_ids = {c.id for c in components}
    for c in components:
        seen_chain, cur, ok = set(), c, True
        while cur is not None and cur.parent is not None:
            if cur.id in seen_chain:
                cta.append(f"cycle through {c.id}")
                ok = False
                break
            seen_chain.add(cur.id)
            cur = by_id.get(cur.parent)
            if cur is None:
                break
        if ok and (cur is None or cur.id not in comp_ids) and c.parent is not None:
            cta.append(f"{c.id}: not reachable from a root")
    rep.rule("spec/component-tree-acyclic", "error", sorted(set(cta)))

    # spec/depends-on-exists  &  spec/depends-on-components-only
    doe, doco = [], []
    for c in components:
        for e in c.fm.get("depends_on", []) or []:
            t = _edge_target(e)
            if t not in by_id:
                doe.append(f"{c.id}: depends_on {t!r} does not exist")
            elif by_id[t].kind != "component":
                doco.append(f"{c.id}: depends_on {t} is a {by_id[t].kind}, not a component")
    rep.rule("spec/depends-on-exists", "error", doe)
    rep.rule("spec/depends-on-components-only", "error", doco)

    # spec/depends-on-acyclic — DAG over depends_on
    graph = {c.id: [_edge_target(e) for e in (c.fm.get("depends_on", []) or [])
                    if _edge_target(e) in by_id] for c in components}
    WHITE, GREY, BLACK = 0, 1, 2
    color = {cid: WHITE for cid in graph}
    cyc = []

    def visit(u):
        color[u] = GREY
        for v in graph.get(u, []):
            if color.get(v) == GREY:
                cyc.append(f"depends_on cycle: {u} → {v}")
            elif color.get(v) == WHITE:
                visit(v)
        color[u] = BLACK

    for cid in graph:
        if color[cid] == WHITE:
            visit(cid)
    rep.rule("spec/depends-on-acyclic", "error", sorted(set(cyc)))

    # spec/touches-exists  &  spec/feature-touches-nonempty
    te, ftn = [], []
    for f in features:
        touches = f.fm.get("touches", []) or []
        if not touches:
            ftn.append(f"{f.id}: touches no component")
        for t in touches:
            comp = t.get("component") if isinstance(t, dict) else None
            if comp not in by_id or by_id[comp].kind != "component":
                te.append(f"{f.id}: touches {comp!r} which is not a component")
    rep.rule("spec/touches-exists", "error", te)
    rep.rule("spec/feature-touches-nonempty", "error", ftn)

    # spec/single-sentence-responsibility / intent
    ssr = [f"{c.id}: responsibility is not one sentence"
           for c in components if not _is_one_sentence(c.fm.get("responsibility", ""))]
    rep.rule("spec/single-sentence-responsibility", "error", ssr)
    ssi = [f"{f.id}: intent is not one sentence"
           for f in features if not _is_one_sentence(f.fm.get("intent", ""))]
    rep.rule("spec/single-sentence-intent", "error", ssi)

    # ---- warnings ----

    # spec/distinct-responsibilities
    by_resp: dict[str, list[str]] = {}
    for c in components:
        by_resp.setdefault((c.fm.get("responsibility") or "").strip(), []).append(c.id)
    dr = [f"shared responsibility: {', '.join(ids)}" for r, ids in by_resp.items() if r and len(ids) > 1]
    rep.rule("spec/distinct-responsibilities", "warn", dr)

    # spec/component-untouched — only meaningful when the spec has features
    if features:
        touched = {t.get("component") for f in features for t in (f.fm.get("touches") or []) if isinstance(t, dict)}
        cu = [f"{c.id}: no feature touches it" for c in components if c.id not in touched]
        rep.rule("spec/component-untouched", "warn", cu)

    # spec/feature-has-acceptance
    fha = [f"{f.id}: empty ## Acceptance" for f in features
           if not f.sections().get("Acceptance")]
    rep.rule("spec/feature-has-acceptance", "warn", fha)

    # spec/core-body-complete
    cbc = []
    for n in nodes:
        if n.fm.get("tier", "core") != "core":
            continue
        secs = n.sections()
        if n.kind == "component" and not (secs.get("Why") or secs.get("Contract")):
            cbc.append(f"{n.id}: core component with empty ## Why and ## Contract")
        if n.kind == "feature" and not secs.get("Behavior"):
            cbc.append(f"{n.id}: core feature with empty ## Behavior")
    rep.rule("spec/core-body-complete", "warn", cbc)

    # spec/decided-has-no-open-questions
    dhoq = [f"{n.id}: decided but has open_questions"
            for n in nodes if n.fm.get("status") == "decided" and n.fm.get("open_questions")]
    rep.rule("spec/decided-has-no-open-questions", "warn", dhoq)

    return rep


def main() -> None:
    spec_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not spec_dir.is_dir():
        print(f"not a directory: {spec_dir}")
        sys.exit(2)
    print(f"specifold-lint {spec_dir}\n")
    lint(spec_dir).render_and_exit()


if __name__ == "__main__":
    main()
