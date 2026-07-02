# MFM Spec format

**Version:** 0.4
**Status:** draft — architecture, features, evaluation notes, and node supersession
**Part of:** [MadeForMachine](https://madeformachine.com)

The MFM Spec format is an agent-native specification format: a way to describe a
software system as a set of files that an agent can read and build from, and a
human can read and reason about. It is the durable artifact — the conversation that
produces it is disposable, and so is any code generated from it. The format is the
thing that persists.

This document is normative. It is the contract that a MFM Spec conforms to.
The executable counterpart is the [reference schema](#reference-schema) at the end;
where prose and schema disagree, the schema wins.

## Scope of v0.4 — architecture, features, evaluations, and supersession

A MFM Spec describes a software system as a graph of **nodes**. v0.4 defines
two durable design node kinds and one lightweight feedback node:

- **components** — the architecture layer (unchanged from v0.1): a tree of
  components, their single responsibilities, the dependencies between them, and the
  reasoning behind the structure.
- **features** — the feature layer (new in v0.2): what the system observably does,
  each feature a path across the components it needs, with the behavior and
  acceptance that hold regardless of how the system is built.
- **evaluations** — documented human or customer feedback about a revision,
  feature, component, variant, or artifact. Evaluations record verdicts and lessons;
  they do not mutate intent by themselves.

The two layers are **peers, not a hierarchy.** Features are not derived from
architecture, nor architecture from features; they constrain each other and
co-evolve. A feature is a path *across* the component tree — it cannot be a property
of any one component — which is precisely why it is its own kind of node, linked to
components rather than nested under one.

v0.4 adds no new node kind. It adds **supersession** to the node lifecycle: a
`superseded` status and a `superseded_by` edge, so a reorganization — a rename, a
merge, a split, a retire — preserves the predecessor's provenance in the graph instead
of hard-deleting it (see [Node lifecycle and supersession](#node-lifecycle-and-supersession)).

v0.4 deliberately does **not** describe:

- technologies, frameworks, or libraries,
- UI/UX layouts or flows,
- data schemas,
- code.

Those are lower layers, reserved for later versions (see [Versioning](#versioning)).
Keeping the spec narrow is what keeps it small, portable across technology choices,
and cheap to throw a new idea at. The version number is a promise that the format
grows downward over time — not that it is finished.

**Earlier specs remain valid.** v0.4 is additive: v0.1 component-only, v0.2
component+feature, and v0.3 component+feature+evaluation specs remain valid, and the
existing rules are unchanged. A spec declares the version it was written against;
tools support the versions they understand.

## A spec is a directory

A MFM Spec is a directory containing:

```
my-system/
  mfm-spec.yaml          # root manifest — declares the format version
  <component>.md          # one file per component
  <component>/            # children of a component mirror the tree as subdirs
    <child-component>.md
  features/               # feature files live here
    <feature>.md
  evaluations/            # feedback/evaluation notes live here
    <evaluation>.md
```

- **One file per node.** Each node is a single Markdown file with YAML frontmatter
  and a prose body.
- **The component directory tree mirrors the component tree.** A component's
  children live in a sibling directory named after it. This is a convenience for
  humans; the authoritative parent/child relationship is the `parent` field, not the
  directory.
- **Features live under `features/`.** A feature crosses the component tree, so it
  does not nest within it. Features may be grouped (an epic and its features) via the
  `parent` field, but their directory placement is not load-bearing.
- **Evaluations live under `evaluations/`.** They are feedback records, not part of
  the component tree and not feature epics. Their `subject` field carries what they
  evaluate.

### Root manifest — `mfm-spec.yaml`

Every spec has exactly one root manifest at its top level. It makes the spec
self-identifying: a tool can read one file and know the format version and entry
point before parsing any node.

```yaml
spec_format: "0.4"        # the MFM Spec format version this spec conforms to
name: "Acme"              # human name of the system being specified
root: ingestion           # id of the root component (the node whose parent is null)
created: 2026-06-18       # ISO date the spec was started
invariants:               # system-wide properties that are no single node's job
  - every inbound item is routed exactly once
```

| field         | type            | required | notes                                              |
|---------------|-----------------|----------|----------------------------------------------------|
| `spec_format` | string          | yes      | exact format version, e.g. `"0.4"`                 |
| `name`        | string          | yes      | the system's human name                            |
| `root`        | component id    | yes      | must match the `id` of the single root component   |
| `created`     | ISO date        | no       | when the spec was started                          |
| `invariants`  | list of strings | no       | system-wide properties that aren't owned by one node |

## A node file

Each node file has two parts, addressed to two audiences:

- **frontmatter** — structured, machine-read; the deterministically-checkable graph
  an agent builds from and a linter validates.
- **body** — prose, human-read; the reasoning that is normally lost when a
  conversation ends.

The split is drawn at one precise line: **everything a tool can verify without
judgment lives in the frontmatter; everything that needs judgment stays in named
prose.** A field earns a place in the frontmatter only when a deterministic check
needs it. This is what keeps a node concise and keeps the validator honest.

Every node carries a `kind`. v0.4 defines `component`, `feature`, and
`evaluation`; future layers (`ux`, `stack`, `plan`) will add kinds without
disturbing these.

### A component file

Components are unchanged from v0.1.

#### Frontmatter

```yaml
---
id: routing-engine
title: Routing engine
kind: component
parent: api-service
responsibility: Decide where each inbound item is delivered.
tier: core
status: open
depends_on: [identity, delivery]
open_questions:
  - sync or async dispatch?
  - retry policy on delivery failure?
---
```

| field            | type                          | required | default | notes                                                                 |
|------------------|-------------------------------|----------|---------|-----------------------------------------------------------------------|
| `id`             | string                        | yes      | —       | stable, lowercase, hyphenated; unique across the spec                 |
| `title`          | string                        | yes      | —       | human-readable name                                                   |
| `kind`           | `component`                   | yes      | —       | the node kind discriminator                                           |
| `parent`         | component id \| `null`        | yes      | —       | the parent's `id`; `null` for exactly one component (the root)        |
| `responsibility` | string                        | yes      | —       | **exactly one sentence** — what this component is responsible for     |
| `tier`           | `core` \| `experimental`      | no       | `core`  | `experimental` marks a component that may not survive                 |
| `status`         | `draft` \| `open` \| `decided` \| `superseded` | no | `draft` | `draft` = sketched, `open` = has unresolved questions, `decided` = settled, `superseded` = retired by a reorganization — see [Node lifecycle and supersession](#node-lifecycle-and-supersession) |
| `depends_on`     | list of edges                 | no       | `[]`    | the components this one needs; see [Dependency edges](#dependency-edges) |
| `superseded_by`  | list of component ids         | no       | `[]`    | successor components of a superseded node; see [Node lifecycle and supersession](#node-lifecycle-and-supersession) |
| `open_questions` | list of strings               | no       | `[]`    | unresolved decisions parked on this component                         |

#### Dependency edges

An entry in `depends_on` is either a bare component id (the v0.1 form) or a typed
edge:

```yaml
depends_on:
  - identity                                  # bare id — still valid
  - { to: delivery, kind: consumes, what: transport channels }
```

`kind` is one of `consumes`, `emits`, `uses`, `configured-by`. Typed edges let the
edge be checked against the component's `## Contract` and let visualization tools
draw each relation differently. Edges always connect components to components.

### A feature file

A feature describes what the system observably does. It is implementation-
independent: its `## Acceptance` is the contract that any implementation — in any
language, on any platform — must satisfy to be the same feature.

#### Frontmatter

```yaml
---
id: refund
title: Refund a payment
kind: feature
parent: null
intent: A customer can reverse a completed purchase and get their money back.
tier: core
status: open
touches:
  - { component: payment,   needs: reverse a captured charge }
  - { component: inventory, needs: restock the returned items }
  - { component: notify,    needs: tell the customer the refund completed }
open_questions:
  - partial refunds, or full only?
---
```

| field            | type                          | required | default | notes                                                                 |
|------------------|-------------------------------|----------|---------|-----------------------------------------------------------------------|
| `id`             | string                        | yes      | —       | stable, lowercase, hyphenated; unique across the spec                 |
| `title`          | string                        | yes      | —       | human-readable name                                                   |
| `kind`           | `feature`                     | yes      | —       | the node kind discriminator                                           |
| `parent`         | feature id \| `null`          | yes      | —       | optional epic grouping; a feature's parent is a feature, never a component |
| `intent`         | string                        | yes      | —       | **exactly one sentence** — what the user/caller can observably do     |
| `tier`           | `core` \| `experimental`      | no       | `core`  | as for components                                                     |
| `status`         | `draft` \| `open` \| `decided` \| `superseded` | no | `draft` | as for components                                                     |
| `touches`        | list of `{component, needs}`  | yes      | —       | **at least one**; the link — see below                                |
| `superseded_by`  | list of feature ids           | no       | `[]`    | successor features of a superseded node; see [Node lifecycle and supersession](#node-lifecycle-and-supersession) |
| `open_questions` | list of strings               | no       | `[]`    | unresolved decisions, including parked mismatches                     |

#### The link: `touches`

`touches` is how a feature connects to the architecture. Each entry is a *demand*: a
`needs` placed on a `component`.

- **`needs` is the capability** — a behavior-level verb phrase. It is the portable,
  invariant part of the link: it must hold of every implementation. It is *essential*.
- **`component` is the binding** — a reference to the component that currently
  satisfies the need. It is the *accidental* part: when an implementation decomposes
  differently, the same `needs` re-binds to a different component.

A feature may reference the current decomposition freely; it must never *demand* one.
"Refund needs a charge reversed" is a capability; "Refund needs a `RefundService`" is
a decomposition, and it does not belong in a feature — it would force that structure
on every implementation and collapse the feature and architecture layers back into one.

A **mismatch** is a `needs` that no component's `responsibility`/`## Contract` can
satisfy. Detecting it requires judgment ("does *reverse a charge* fall under
*capture and settle payments*?"), so it is the agent's job, not a lint rule (see
[Integrity and lint rules](#integrity-and-lint-rules)). An unresolved mismatch is
parked as an `open_question`, like any other tension.

### Node lifecycle and supersession

A node's `id` is its identity. When a reorganization changes that identity — a rename,
a merge of several nodes into one, a split of one node into several, or an outright
retire — the predecessor is not deleted. It is **superseded**: its `status` becomes
`superseded` and its `superseded_by` lists the successor node(s), so the fact that the
old node's responsibility now lives elsewhere is a graph fact a tool can traverse, not
prose in a commit message.

```yaml
# resolution-policy.md, after being merged into resolution-lifecycle
status: superseded
superseded_by: [resolution-lifecycle]
```

- **Rename / merge** — the predecessor names exactly one successor.
- **Split** — the predecessor names each of the nodes it divided into.
- **Retire** — the predecessor names no successor (`superseded_by` absent or empty):
  the responsibility is gone, not relocated.

`superseded_by` connects nodes of the **same kind** (component→component,
feature→feature), and only a `superseded` node may carry it — both checked by lint.
Evaluations are never superseded; they are historical records, not design nodes.

A superseded node stays in the graph as provenance, but it is retired from the live
design: no live node's `parent`, `depends_on`, or `touches` should still point at it —
a reorganization repoints every referrer to the successor, and a leftover edge into
the graveyard is flagged (`spec/live-edge-to-superseded`). Evaluations are exempt:
their `subject` legitimately keeps naming the node that existed when the judgment was
made.

### Body

The body is Markdown. Certain sections are part of the format because they carry the
*why*, the *interface*, and the *behavior* — the most valuable and most perishable
content in the whole spec. Each section must be **self-contained**: a consumer that
pulls one section must not need another to make sense of it. That is what lets an
agent or a visualization tool pull exactly the sections it needs and nothing more.

Components:

| section                      | required    | purpose                                                              |
|------------------------------|-------------|----------------------------------------------------------------------|
| `## Why`                     | recommended | why this component exists as its own unit, and why it is shaped so   |
| `## Contract`                | recommended | what it provides and consumes — write as `Provides: …` / `Consumes: …` |
| `## Essential vs accidental` | optional    | what is intrinsic to the component vs an incidental, lower-level choice |
| `## Rejected`                | optional    | alternatives considered and why they lose — the entanglements avoided |
| `## Decisions`               | optional    | resolved `open_questions`: the choice and why, kept instead of deleted |

Features:

| section          | required    | purpose                                                              |
|------------------|-------------|----------------------------------------------------------------------|
| `## Behavior`    | recommended | what happens, end to end — the narrative of the feature              |
| `## Acceptance`  | recommended | the implementation-independent equivalence contract — what any build must satisfy |
| `## Rejected`    | optional    | alternative behaviors considered and why they lose                   |
| `## Decisions`   | optional    | resolved `open_questions`: the choice and why                        |

A `core` node with a crisp `responsibility`/`intent` but an empty body is a ticket,
not a spec node. It records *what* without preserving *why the system is shaped this
way*. Tools should warn (see `spec/core-body-complete`).

### Worked example — a feature

`features/refund.md`:

```markdown
---
id: refund
title: Refund a payment
kind: feature
parent: null
intent: A customer can reverse a completed purchase and get their money back.
tier: core
status: open
touches:
  - { component: payment,   needs: reverse a captured charge }
  - { component: inventory, needs: restock the returned items }
  - { component: notify,    needs: tell the customer the refund completed }
open_questions:
  - partial refunds, or full only?
---

## Behavior
Given a completed order, when a refund is requested within the allowed window, the
money returns to the original method, stock is restored, and the customer is told.

## Acceptance
- A refund never exceeds the original charge.
- Stock is restored exactly once, even if notify fails.

## Rejected
Store credit instead of money-back — changes the user's mental model of "refund."
```

### An evaluation file

An evaluation records feedback or judgment about something derived from, described by,
or revised within the spec. It is intentionally small: a verdict, a one-sentence
summary, and optional evidence/lessons. The human remains the evaluator; the spec is
where that judgment stops evaporating.

#### Frontmatter

```yaml
---
id: refund-v1-evaluation
title: Refund v1 evaluation
kind: evaluation
subject:
  feature: refund
  rev: "2026-06-29T12-15-00Z"
verdict: mixed
summary: Customers understood refunds but expected partial refunds from day one.
evidence:
  - three customer interviews
  - support-ticket review
promotes_to_spec:
  - Partial refunds are a core behavior, not a later payment-provider detail.
rejects:
  - Full-refund-only MVP.
---
```

| field              | type                                      | required | default | notes                                      |
|--------------------|-------------------------------------------|----------|---------|--------------------------------------------|
| `id`               | string                                    | yes      | —       | stable, lowercase, hyphenated              |
| `title`            | string                                    | yes      | —       | human-readable name                        |
| `kind`             | `evaluation`                              | yes      | —       | the node kind discriminator                |
| `subject`          | object                                    | yes      | —       | what was evaluated; see below              |
| `verdict`          | `accepted` \| `rejected` \| `mixed` \| `observed` | yes | — | the evaluation result                      |
| `summary`          | string                                    | yes      | —       | **exactly one sentence**                   |
| `evidence`         | list of strings                           | no       | `[]`    | sources for the judgment                   |
| `promotes_to_spec` | list of strings                           | no       | `[]`    | lessons that should affect the spec        |
| `rejects`          | list of strings                           | no       | `[]`    | ideas, variants, or behaviors ruled out    |

`subject` must name at least one thing being evaluated. `feature` and `component`
references are checked when present; `rev`, `variant`, and `artifact` are labels the
tool records but does not resolve in v0.4.

```yaml
subject:
  feature: refund
  component: payment
  rev: "abc123"
  variant: fastapi-postgres
  artifact: demo-build-2026-06-29
```

#### Body

| section       | required    | purpose                                                   |
|---------------|-------------|-----------------------------------------------------------|
| `## Notes`    | recommended | what was seen, heard, or judged                           |
| `## Evidence` | optional    | links, quotes, test runs, interview references            |
| `## Decision` | optional    | what changed in the spec because of this evaluation       |

Evaluations are not a full back-loop protocol. They are the minimal durable memory
for feedback while the product remains focused on authoring, evolving, validating,
and slicing specs.

## Integrity and lint rules

A spec's structure is checked by deterministic rules over the graph — frontmatter
and cross-file references, never prose. Each rule has a stable id so the OSS linter
and a hosted store enforce the same thing. `error` means the spec is invalid;
`warn` means it is valid but flagged.

| rule id | sev | checks |
|---|---|---|
| `spec/declared-format` | error | `mfm-spec.yaml` exists; `spec_format` is a version the tool understands |
| `spec/kind-known` | error | every node's `kind` is one the tool understands |
| `spec/unique-ids` | error | no two nodes share an `id` |
| `spec/single-root` | error | exactly one component has `parent: null`; the manifest's `root` names it |
| `spec/parent-exists` | error | every non-root `parent` resolves to a node |
| `spec/parent-same-kind` | error | a node's `parent` is the same `kind` (component→component, feature→feature) |
| `spec/component-tree-acyclic` | error | `parent` links form a tree; every component is reachable from the root |
| `spec/depends-on-exists` | error | every `depends_on` target resolves |
| `spec/depends-on-components-only` | error | `depends_on` connects components to components only |
| `spec/depends-on-acyclic` | error | the `depends_on` graph is a DAG |
| `spec/touches-exists` | error | every `touches[].component` resolves to a component |
| `spec/feature-touches-nonempty` | error | every feature touches at least one component |
| `spec/evaluation-shape` | error | every evaluation has a non-empty `subject` and a valid `verdict` |
| `spec/evaluation-subject-exists` | error | every `subject.feature` / `subject.component` reference resolves to the right node kind |
| `spec/superseded-by-exists` | error | every `superseded_by` target resolves to a node of the same kind |
| `spec/superseded-shape` | error | only a node with `status: superseded` carries `superseded_by` |
| `spec/single-sentence-responsibility` | error | `responsibility` is one sentence |
| `spec/single-sentence-intent` | error | `intent` is one sentence |
| `spec/single-sentence-summary` | error | evaluation `summary` is one sentence |
| `spec/distinct-responsibilities` | warn | no two **live** components declare the same `responsibility` (a superseded node keeps its responsibility as provenance) |
| `spec/component-untouched` | warn | a live **leaf** component no feature touches — a missing feature, or over-architecture; grouping parents and superseded components are exempt |
| `spec/live-edge-to-superseded` | warn | a live node's `parent`, `depends_on`, or `touches` targets a superseded node — a repoint missed by a reorganization; evaluation subjects are exempt |
| `spec/feature-has-acceptance` | warn | a feature has a non-empty `## Acceptance` |
| `spec/core-body-complete` | warn | a `core` node has a non-empty `## Why`/`## Contract` (or `## Behavior` for features) |
| `spec/decided-has-no-open-questions` | warn | a node marked `decided` carries no `open_questions` |

Reserved for v0.4: `spec/variant-invariance` — fields marked invariant agree across
implementation variants.

Validity is structural, not aesthetic. It says the graph hangs together; it does not
say the architecture is good. **Semantic checks are deliberately not lint rules** —
whether a feature's `needs` is satisfied by a component's responsibility, whether two
features contradict, whether a feature's coordination is owned by some component — all
require judgment and are the agent's job. Drawing that line is what keeps this layer
deterministic.

## Versioning

The format version is declared per spec in `mfm-spec.yaml`, not per file.

- **0.x is unstable.** Fields may be added, renamed, or removed between minor
  versions while the format finds its shape. Specs declare the version they were
  written against so tools can migrate or reject them.
- **The format grows downward, additively.** 0.2 added the feature layer as a new
  node kind, 0.3 added evaluations as lightweight feedback records, and 0.4 added
  supersession to the node lifecycle, without disturbing the architecture layer.
  Future versions are expected to add a UI/UX layer, a technology-binding layer, and
  a data-shape layer the same way. A spec written against an earlier version stays
  valid.
- **A version is a promise about scope, not a claim of completeness.** Calling this
  0.4 says plainly: this describes architecture, features, evaluation notes, and how
  nodes are retired, and nothing below them, today.

## Reference schema

The normative, executable form of the frontmatter and root manifest is the pair of
JSON Schema files alongside this document:

- [`mfm-spec.schema.json`](mfm-spec.schema.json) — a single node's frontmatter (`oneOf`
  component / feature / evaluation)
- [`mfm-spec-manifest.schema.json`](mfm-spec-manifest.schema.json) — the `mfm-spec.yaml` manifest

JSON Schema validates *shape* only — types, required fields, enums, reference format.
Cross-spec integrity (uniqueness, reference existence, single root, acyclicity, the
feature/component link) is enforced by the [lint rules](#integrity-and-lint-rules)
over the full graph, not by the per-node schema. Where prose and schema disagree, the
schema wins.

A Pydantic v2 transcription, for convenience:

```python
from datetime import date
from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field


class Tier(str, Enum):
    core = "core"
    experimental = "experimental"


class Status(str, Enum):
    draft = "draft"
    open = "open"
    decided = "decided"
    superseded = "superseded"      # retired by a reorganization; see superseded_by


class Edge(BaseModel):
    """A typed dependency edge; a bare id string is also accepted in YAML."""
    to: str
    kind: Literal["consumes", "emits", "uses", "configured-by"] | None = None
    what: str | None = None


class Touch(BaseModel):
    """One entry in a feature's `touches` — a demand on a component."""
    component: str                 # the binding (accidental, re-projectable)
    needs: str                     # the capability (essential, invariant)


class EvaluationSubject(BaseModel):
    """What an evaluation is about. feature/component refs are checked by lint."""
    feature: str | None = None
    component: str | None = None
    rev: str | None = None
    variant: str | None = None
    artifact: str | None = None


class SpecRoot(BaseModel):
    """The `mfm-spec.yaml` root manifest."""
    spec_format: str
    name: str
    root: str                      # id of the root component
    created: date | None = None
    invariants: list[str] = Field(default_factory=list)


class Component(BaseModel):
    """A component node's frontmatter."""
    id: str                        # stable, lowercase, hyphenated, unique
    title: str
    kind: Literal["component"] = "component"
    parent: str | None             # parent id, or None for the root
    responsibility: str            # exactly one sentence
    tier: Tier = Tier.core
    status: Status = Status.draft
    depends_on: list[str | Edge] = Field(default_factory=list)
    superseded_by: list[str] = Field(default_factory=list)  # successors of a superseded node
    open_questions: list[str] = Field(default_factory=list)


class Feature(BaseModel):
    """A feature node's frontmatter."""
    id: str
    title: str
    kind: Literal["feature"] = "feature"
    parent: str | None             # a feature id (epic) or None
    intent: str                    # exactly one sentence
    tier: Tier = Tier.core
    status: Status = Status.draft
    touches: list[Touch] = Field(min_length=1)
    superseded_by: list[str] = Field(default_factory=list)  # successors of a superseded node
    open_questions: list[str] = Field(default_factory=list)


class Evaluation(BaseModel):
    """A feedback or judgment node."""
    id: str
    title: str
    kind: Literal["evaluation"] = "evaluation"
    subject: EvaluationSubject
    verdict: Literal["accepted", "rejected", "mixed", "observed"]
    summary: str
    evidence: list[str] = Field(default_factory=list)
    promotes_to_spec: list[str] = Field(default_factory=list)
    rejects: list[str] = Field(default_factory=list)
```

Cross-node integrity is enforced over the full set of nodes, not by the per-node
models above — see [Integrity and lint rules](#integrity-and-lint-rules).
