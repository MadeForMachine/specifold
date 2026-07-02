---
name: mfm-spec
description: >-
  Use when working with hosted MFM Spec: a spec stored in the MadeForMachine service
  and read, mutated, validated, and versioned through MCP tools. Use for
  service-backed spec authoring, minimal-context reads,
  fine-grained spec mutations, validation, history, and evaluation notes. Do not use
  for local file-backed specs; use the mfm-spec-local skill for that.
version: 0.3.0
status: alpha
public: true
connector: mfm
requires: [mfm_spec_read, mfm_spec_validate, mfm_spec_mutate, mfm_spec_rename, mfm_spec_merge, mfm_spec_split, mfm_spec_retire, mfm_spec_write, mfm_spec_history, mfm_spec_import, mfm_spec_export]
license: MIT
---

# MFM Spec

MFM Spec is the hosted MadeForMachine product that uses the MFM Spec format as its
portable artifact, but keeps the canonical working spec in a service-backed revision store.
Your job is to steer the user's own agent: discuss, interrogate, read minimal context,
mutate through deterministic MCP tools, and let server validation guard the graph.

If the `mfm_spec_*` MCP tools are not available, do not pretend to persist anything. You may
shape the intended change in the conversation, but stop before commit and report that the
MFM Spec connector/tooling is missing.

## Scope

Work at the MFM Spec MVP graph level:

- **Components** — responsibility owners.
- **Features** — observable behavior linked to the components they need.
- **Evaluations** — feedback or judgment records against a feature, component, revision,
  variant, or artifact.

Do not choose technologies, UI layouts, data schemas, implementation plans, or code. Park
those as lower-layer details or open questions on the relevant node.

## Read Small

Start every session with `mfm_spec_read` using `view=map`. Keep the whole map in context:
node id, kind, status, parent, and edge summary. Load full bodies only for the active blast
radius:

- `view=node` for one full node,
- `view=subtree` for a component branch,
- `view=referrers` for everything pointing AT one node — children, dependents, touching
  features, evaluation subjects — the blast radius to query before any identity change,
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

The normal commit path is `mfm_spec_mutate`, not whole-node replacement. Use
`mfm_spec_validate` first when the change is non-trivial or when you expect a repair loop.
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

Use `mfm_spec_write` only for import/bootstrap or as an escape hatch when the user already
intends to replace whole nodes. It is not the normal authoring primitive.

## Reorganize Through Intents, Not Cascades

A node's id is its identity. When the shape of the spec is wrong — a node is misnamed, two
nodes are one, one node is two, a responsibility is gone — do NOT hand-compose the change
from primitive ops, and never end an identity change in `delete_node`: that destroys the
provenance the graph is for. Use the dedicated intents:

- `mfm_spec_rename` — recreates under the new id, repoints every live referrer, supersedes
  the old id. Fully deterministic; you supply nothing but the ids.
- `mfm_spec_merge` — you author the successor (`into`: a create payload, or an existing
  node id to absorb into); the server wires: referrers repoint, each merged node gets
  `status: superseded` and `superseded_by` → successor.
- `mfm_spec_split` — you author the successor payloads and `reassign` each live referrer to
  the successor it now needs; the server refuses to guess an unassigned referrer.
- `mfm_spec_retire` — for a responsibility that is gone, not relocated. Refused while live
  nodes still reference it; the refusal lists them.

The loop is always: `view=referrers` on the affected node → name the blast radius to the
user → issue the intent with the current `base_rev`. Superseded nodes stay in the graph as
provenance; evaluations keep pointing at them by design.

If a write is rejected because `base_rev` is stale, re-read the map and the changed nodes,
reconcile the user's intent against the new head, and resend a fresh mutation batch. Never
force through a conflict.

## Validation Boundary

`mfm_spec_validate` and `mfm_spec_mutate` both apply the proposed operations to the base
revision, parse the resulting MFM Spec graph, and run the deterministic lint rules. A
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
