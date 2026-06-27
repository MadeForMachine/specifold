# Specifold Format

**Version:** 0.2
**Status:** draft — the architecture layer and the feature layer
**Part of:** [MadeForMachine](https://madeformachine.com)

The Specifold Format is an agent-native specification format: a way to describe a
software system as a set of files that an agent can read and build from, and a
human can read and reason about. It is the durable artifact — the conversation that
produces it is disposable, and so is any code generated from it. The format is the
thing that persists.

This document is normative. It is the contract that a Specifold spec conforms to.
The executable counterpart is the [reference schema](#reference-schema) at the end;
where prose and schema disagree, the schema wins.

## Scope of v0.2 — architecture and features

A Specifold spec describes a software system as a graph of **nodes**. v0.2 defines
two kinds of node:

- **components** — the architecture layer (unchanged from v0.1): a tree of
  components, their single responsibilities, the dependencies between them, and the
  reasoning behind the structure.
- **features** — the feature layer (new in v0.2): what the system observably does,
  each feature a path across the components it needs, with the behavior and
  acceptance that hold regardless of how the system is built.

The two layers are **peers, not a hierarchy.** Features are not derived from
architecture, nor architecture from features; they constrain each other and
co-evolve. A feature is a path *across* the component tree — it cannot be a property
of any one component — which is precisely why it is its own kind of node, linked to
components rather than nested under one.

v0.2 deliberately does **not** describe:

- technologies, frameworks, or libraries,
- UI/UX layouts or flows,
- data schemas,
- code.

Those are lower layers, reserved for later versions (see [Versioning](#versioning)).
Keeping the spec narrow is what keeps it small, portable across technology choices,
and cheap to throw a new idea at. The version number is a promise that the format
grows downward over time — not that it is finished.

**v0.1 specs remain valid.** v0.2 is additive: a spec containing only components is
a valid v0.2 spec, and the architecture-layer rules are unchanged. A spec declares
the version it was written against; tools support the versions they understand.

## A spec is a directory

A Specifold spec is a directory containing:

```
my-system/
  specifold.yaml          # root manifest — declares the format version
  <component>.md          # one file per component
  <component>/            # children of a component mirror the tree as subdirs
    <child-component>.md
  features/               # feature files live here
    <feature>.md
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

### Root manifest — `specifold.yaml`

Every spec has exactly one root manifest at its top level. It makes the spec
self-identifying: a tool can read one file and know the format version and entry
point before parsing any node.

```yaml
spec_format: "0.2"        # the Specifold Format version this spec conforms to
name: "Acme"              # human name of the system being specified
root: ingestion           # id of the root component (the node whose parent is null)
created: 2026-06-18       # ISO date the spec was started
invariants:               # system-wide properties that are no single node's job
  - every inbound item is routed exactly once
```

| field         | type            | required | notes                                              |
|---------------|-----------------|----------|----------------------------------------------------|
| `spec_format` | string          | yes      | exact format version, e.g. `"0.2"`                 |
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

Every node carries a `kind`. v0.2 defines `component` and `feature`; future layers
(`ux`, `stack`, `plan`) will add kinds without disturbing these two.

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
| `status`         | `draft` \| `open` \| `decided`| no       | `draft` | `draft` = sketched, `open` = has unresolved questions, `decided` = settled |
| `depends_on`     | list of edges                 | no       | `[]`    | the components this one needs; see [Dependency edges](#dependency-edges) |
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
| `status`         | `draft` \| `open` \| `decided`| no       | `draft` | as for components                                                     |
| `touches`        | list of `{component, needs}`  | yes      | —       | **at least one**; the link — see below                                |
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

## Integrity and lint rules

A spec's structure is checked by deterministic rules over the graph — frontmatter
and cross-file references, never prose. Each rule has a stable id so the OSS linter
and a hosted store enforce the same thing. `error` means the spec is invalid;
`warn` means it is valid but flagged.

| rule id | sev | checks |
|---|---|---|
| `spec/declared-format` | error | `specifold.yaml` exists; `spec_format` is a version the tool understands |
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
| `spec/single-sentence-responsibility` | error | `responsibility` is one sentence |
| `spec/single-sentence-intent` | error | `intent` is one sentence |
| `spec/distinct-responsibilities` | warn | no two components declare the same `responsibility` |
| `spec/component-untouched` | warn | a component no feature touches — a missing feature, or over-architecture |
| `spec/feature-has-acceptance` | warn | a feature has a non-empty `## Acceptance` |
| `spec/core-body-complete` | warn | a `core` node has a non-empty `## Why`/`## Contract` (or `## Behavior` for features) |
| `spec/decided-has-no-open-questions` | warn | a node marked `decided` carries no `open_questions` |

Reserved for v0.3: `spec/variant-invariance` — fields marked invariant agree across
implementation variants.

Validity is structural, not aesthetic. It says the graph hangs together; it does not
say the architecture is good. **Semantic checks are deliberately not lint rules** —
whether a feature's `needs` is satisfied by a component's responsibility, whether two
features contradict, whether a feature's coordination is owned by some component — all
require judgment and are the agent's job. Drawing that line is what keeps this layer
deterministic.

## Versioning

The format version is declared per spec in `specifold.yaml`, not per file.

- **0.x is unstable.** Fields may be added, renamed, or removed between minor
  versions while the format finds its shape. Specs declare the version they were
  written against so tools can migrate or reject them.
- **The format grows downward, additively.** 0.2 added the feature layer as a new
  node kind, without disturbing the architecture layer. Future versions are expected
  to add a UI/UX layer, a technology-binding layer, and a data-shape layer the same
  way. A spec written against an earlier version stays valid.
- **A version is a promise about scope, not a claim of completeness.** Calling this
  0.2 says plainly: this describes architecture and features, and nothing below them,
  today.

## Reference schema

The normative, executable form of the frontmatter and root manifest is the pair of
JSON Schema files alongside this document:

- [`node.schema.json`](node.schema.json) — a single node's frontmatter (`oneOf`
  component / feature)
- [`manifest.schema.json`](manifest.schema.json) — the `specifold.yaml` manifest

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


class Edge(BaseModel):
    """A typed dependency edge; a bare id string is also accepted in YAML."""
    to: str
    kind: Literal["consumes", "emits", "uses", "configured-by"] | None = None
    what: str | None = None


class Touch(BaseModel):
    """One entry in a feature's `touches` — a demand on a component."""
    component: str                 # the binding (accidental, re-projectable)
    needs: str                     # the capability (essential, invariant)


class SpecRoot(BaseModel):
    """The `specifold.yaml` root manifest."""
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
    open_questions: list[str] = Field(default_factory=list)
```

Cross-node integrity is enforced over the full set of nodes, not by the per-node
models above — see [Integrity and lint rules](#integrity-and-lint-rules).
