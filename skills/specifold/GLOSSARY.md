# Specifold glossary

> Part of **MadeForMachine** · [madeformachine.com](https://madeformachine.com)

The vocabulary of Specifold, defined once. Terms fall into three groups: the
**artifact** (what a spec is made of), **retrieval** (how slices of it are read and
turned into outputs), and the **system** (the components that do the work). One rule
runs through all of it: **only the canonical store is authoritative; everything else
is derived from it and can be rebuilt.**

## The artifact

- **Spec** — the complete specification of one system: a set of *nodes* and the
  *edges* between them. Stored as markdown files in a project folder. Unqualified, "spec" means a
  *product spec*.
- **Format spec** — the definition of the Specifold format itself: `SPEC.md`, the
  JSON Schemas, and the reference parser and lint. The rules every spec obeys. Lives
  in the public `specifold` repo; this glossary is part of it.
- **Product spec** — a concrete spec *written in* the format, describing one product
  or system (e.g. MadeForMachine's own, at `madeformachine/spec/`). An instance, not
  the rules. A product spec is private to whoever owns the product it describes.
- **Node** — one unit of a spec, stored as one file, with structured *frontmatter*
  and a prose *body*. Every node is a *component*, *feature*, or *evaluation*.
- **Component** — a node describing a piece of the architecture: one responsibility,
  its dependencies, and the reasoning behind it.
- **Feature** — a node describing an observable behaviour: an intent, the components
  it *touches*, and the acceptance any implementation must satisfy.
- **Evaluation** — a node recording feedback or judgment about a feature,
  component, revision, variant, or artifact. It preserves what was learned; it does
  not mutate intent by itself.
- **Section** — a named part of a node's body (`## Why`, `## Contract`,
  `## Acceptance`, …). A body is a set of sections.
- **Edge** — a typed link between nodes: a component's `depends_on`, or a feature's
  `touches`.
- **Canonical store** — the markdown files in the project spec directory. The single
  source of truth for local Specifold, and the only authoritative thing in the system.

## Retrieval

All of these are *derived from* the canonical store.

- **Materialize** — parse the canonical store into the read-model.
- **Read-model** — the spec as a queryable graph (id → node, plus adjacency and
  reverse indices). Exists so queries don't re-parse files each time. Never
  authoritative; rebuilt when files change. Held in memory at MVP scale.
- **Cell** — the atom of retrieval: one *(node, section)* pair, addressed
  `node-id#section-slug` (e.g. `payment#contract`). `node-id#frontmatter` addresses
  the structured fields.
- **Index** — a lightweight map of the whole spec — every node's id, summary, edges,
  and section *names*, but no section bodies. Cheap to load whole; used to plan a
  retrieval. A thin view of the read-model.
- **Projection** — a named, saved query: a node-filter × a section-filter
  (e.g. `code-derivation` = (features + components) × (`contract`, `acceptance`)).
- **Pull** — execute a projection against the read-model and return a bundle of cells.
- **Derivation** — run the cells from a pull through a template and a model to produce
  an *artifact*. A pull gets the right slice; a derivation turns it into something new.
- **Artifact** — a generated downstream output of a derivation: a UI/UX prompt, an
  architecture brief, a stack-bound plan. Disposable; regenerable from the spec.

## The system

The components that do the work.

- **Reference linter** — the deterministic checker that validates local Specifold files.
- **MrSpec** — the separate hosted MadeForMachine product that stores Specifold specs in a
  database and exposes them through MCP. It is not the local Specifold skill.
