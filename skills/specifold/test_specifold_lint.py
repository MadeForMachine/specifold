#!/usr/bin/env python3
"""Tests for the in-memory linting API (parse_node / parse_manifest / lint_nodes).

This is the surface the hosted Specifold store consumes: it never touches the
filesystem, so these build nodes from text and lint them directly. Run with
`python3 test_specifold_lint.py` (no pytest needed) or under pytest.
"""

from __future__ import annotations

from specifold_lint import lint_nodes, parse_manifest, parse_node

MANIFEST = parse_manifest('spec_format: "0.3"\nname: "T"\nroot: root\n')


def node(id_, parent, *, resp="Does exactly one thing.", kind="component", extra=""):
    parent_yaml = "null" if parent is None else parent
    return parse_node(
        f"---\nid: {id_}\ntitle: {id_}\nkind: {kind}\nparent: {parent_yaml}\n"
        f"responsibility: {resp}\n{extra}---\n\n## Why\nbecause.\n"
    )


def errors(rep):
    return {e["rule"] for e in rep.summary()["errors"]}


def feature(id_, *, component="root"):
    return parse_node(
        f"---\nid: {id_}\ntitle: {id_}\nkind: feature\nparent: null\n"
        f"intent: A caller can do one thing.\ntouches:\n"
        f"  - {{ component: {component}, needs: support the feature }}\n"
        "---\n\n## Behavior\nIt happens.\n\n## Acceptance\n- It works.\n"
    )


def evaluation(id_, *, subject="feature: feat", summary="The trial taught one thing."):
    return parse_node(
        f"---\nid: {id_}\ntitle: {id_}\nkind: evaluation\n"
        f"subject:\n  {subject}\nverdict: mixed\nsummary: {summary}\n"
        "---\n\n## Notes\nUseful feedback.\n"
    )


def test_parse_node_skips_non_nodes():
    assert parse_node("# just prose\n\nno frontmatter") is None
    assert parse_node("---\ntitle: x\n---\nbody") is None  # no id
    n = parse_node("---\nid: a\ntitle: A\nparent: null\nresponsibility: x.\n---\n")
    assert n is not None and n.id == "a"
    assert n.kind == "component"  # v0.1 default applied


def test_clean_spec_has_no_errors():
    rep = lint_nodes([node("root", None), node("child", "root")], MANIFEST)
    assert not rep.has_errors(), rep.summary()
    assert errors(rep) == set()


def test_catches_structural_breakage():
    # duplicate id, a dangling parent, a dangling depends_on, two roots
    nodes = [
        node("root", None),
        node("root", None),  # duplicate id + second root
        node("orphan", "ghost"),  # parent does not exist
        node("dep", "root", extra="depends_on: [missing]\n"),  # dangling edge
    ]
    e = errors(lint_nodes(nodes, MANIFEST))
    assert "spec/unique-ids" in e
    assert "spec/single-root" in e
    assert "spec/parent-exists" in e
    assert "spec/depends-on-exists" in e


def test_unknown_kind_is_an_error():
    weird = parse_node("---\nid: odd\ntitle: Odd\nkind: odd\n---\n")
    assert "spec/kind-known" in errors(lint_nodes([node("root", None), weird], MANIFEST))


def test_multi_sentence_responsibility_is_an_error():
    rep = lint_nodes([node("root", None, resp="Does this. And also that.")], MANIFEST)
    assert "spec/single-sentence-responsibility" in errors(rep)


def test_missing_manifest_is_an_error():
    rep = lint_nodes([node("root", None)], None, manifest_problems=["no manifest"])
    assert "spec/declared-format" in errors(rep)


def test_summary_shape_separates_severities():
    # a core component with an empty body trips a warn, not an error
    bare = parse_node("---\nid: root\ntitle: R\nparent: null\nresponsibility: x.\n---\n")
    s = lint_nodes([bare], MANIFEST).summary()
    assert s["errors"] == []
    assert any(w["rule"] == "spec/core-body-complete" for w in s["warnings"])


def test_evaluation_subject_refs_existing_nodes():
    rep = lint_nodes([node("root", None), feature("feat"), evaluation("eval")], MANIFEST)
    assert "spec/evaluation-subject-exists" not in errors(rep)

    bad = lint_nodes([node("root", None), evaluation("eval", subject="feature: missing")], MANIFEST)
    assert "spec/evaluation-subject-exists" in errors(bad)


def test_malformed_evaluation_is_an_error():
    bad = parse_node(
        "---\nid: eval\ntitle: Eval\nkind: evaluation\nsubject: {}\nverdict: nope\n"
        "summary: One thing.\n---\n"
    )
    assert "spec/evaluation-shape" in errors(lint_nodes([node("root", None), bad], MANIFEST))


def test_multi_sentence_evaluation_summary_is_an_error():
    rep = lint_nodes(
        [node("root", None), feature("feat"), evaluation("eval", summary="Good. Bad.")],
        MANIFEST,
    )
    assert "spec/single-sentence-summary" in errors(rep)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"  ✓ {fn.__name__}")
    print(f"\nOK — {len(fns)} passed")
