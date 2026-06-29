---
name: mrspec
description: >-
  Use when working with a hosted MrSpec specification: a Specifold-format spec stored
  in the MadeForMachine service and read, mutated, validated, and versioned through
  MCP tools. Use for service-backed spec authoring, minimal-context reads,
  fine-grained spec mutations, validation, history, and evaluation notes. Do not use
  for local file-backed specs; use the Specifold skill for that.
version: 0.1.0
status: alpha
public: false
connector: mfm
requires: [mrspec_read, mrspec_validate, mrspec_mutate, mrspec_write, mrspec_history]
license: MIT
---

# MrSpec

MrSpec is the hosted MadeForMachine product that uses the Specifold format as its
portable artifact, but keeps the canonical working spec in a service-backed revision store.
Your job is to steer the user's own agent: discuss, interrogate, read minimal context,
mutate through deterministic MCP tools, and let server validation guard the graph.

If the `mrspec_*` MCP tools are not available, do not pretend to persist anything. You may
shape the intended change in the conversation, but stop before commit and report that the
MrSpec connector/tooling is missing.

## Scope

Work at the Specifold MVP graph level:

- **Components** — responsibility owners.
- **Features** — observable behavior linked to the components they need.
- **Evaluations** — feedback or judgment records against a feature, component, revision,
  variant, or artifact.

Do not choose technologies, UI layouts, data schemas, implementation plans, or code. Park
those as lower-layer details or open questions on the relevant node.

## Read Small

Start every session with `mrspec_read` using `view=map`. Keep the whole map in context:
node id, kind, status, parent, and edge summary. Load full bodies only for the active blast
radius:

- `view=node` for one full node,
- `view=subtree` for a component branch,
- named projections such as `authoring-map`, `feature-work`, or `derivation-context` when
  the task has a stable slice shape.

The persisted spec is the memory. The chat is disposable.

## Interrogate First

Let the user dump raw intent before formalizing. Classify it into components, features,
evaluations, open questions, and lower-layer details. Propose the smallest touched node set,
then surface the one or two boundary questions that would change the graph.

Always name the touched nodes before mutating. A request rarely affects one node; trace the
blast radius across dependencies, feature touches, and evaluation subjects.

## Mutate Through Tools

The normal commit path is `mrspec_mutate`, not whole-node replacement. Use
`mrspec_validate` first when the change is non-trivial or when you expect a repair loop.
Every mutation carries the `base_rev` from the last read.

MVP operations are deliberately small and deterministic:

- create node,
- delete node,
- move node,
- set frontmatter field,
- add/remove dependency,
- add/remove feature touch,
- replace or append a named body section,
- record evaluation node.

Use `mrspec_write` only for import/bootstrap or as an escape hatch when the user already
intends to replace whole nodes. It is not the normal authoring primitive.

If a write is rejected because `base_rev` is stale, re-read the map and the changed nodes,
reconcile the user's intent against the new head, and resend a fresh mutation batch. Never
force through a conflict.

## Validation Boundary

`mrspec_validate` and `mrspec_mutate` both apply the proposed operations to the base
revision, parse the resulting Specifold graph, and run the deterministic lint rules. A
failed validation changes nothing. Treat the error report as the source of truth for
structural validity; semantic quality remains your job.

Load-bearing errors:

- exactly one root component,
- all parents, dependencies, feature touches, and checked evaluation subjects resolve,
- component and dependency graphs are acyclic,
- component responsibilities, feature intents, and evaluation summaries are one sentence.

## Evaluation Notes

When feedback arrives, record it as an `evaluation` node instead of burying it in chat or
rewriting intent silently. Evaluations may point at a component, feature, revision, variant,
artifact, or any combination. They record what was learned; a later explicit mutation
promotes that lesson into the spec.
