# Changelog — mfm-spec

## 0.3.0 — 2026-07-02
**MAJOR.** Reorganization becomes first-class: intents, not hand-composed cascades.
- New required tools: `mfm_spec_rename`, `mfm_spec_merge`, `mfm_spec_split`,
  `mfm_spec_retire` — deterministic server-side macros over the primitive ops; the agent
  authors content (a merged responsibility, a split's division), the server does the wiring.
- New `view=referrers` on `mfm_spec_read`: everything pointing at one node — the blast
  radius to query before any identity change.
- Identity changes supersede the predecessor (`status: superseded`, `superseded_by`)
  instead of deleting it, per MFM Spec format v0.4; provenance stays queryable.
- Driven by the reorg dogfood (`mfm-spec-reorg-dogfood`): a rename was a hand-traced 6-op
  cascade, a merge 15 ops ending in a provenance-destroying delete.

## 0.2.1 — 2026-06-30
- Publishes the hosted MFM Spec skill for pilot setup.
- Adds `mfm_spec_import` and `mfm_spec_export` to the declared tool requirements.
- Documents that installation needs both the skill and the authenticated `mfm` MCP server.

## 0.2.0 — 2026-06-29
- Renames the hosted skill from `mrspec` to `mfm-spec`.
- Renames required MCP tools from `mrspec_*` to `mfm_spec_*`.
- Points local file-backed work to `mfm-spec-local`.

## 0.1.0 — 2026-06-29
- Initial alpha hosted-skill split from local MFM Spec.
- Defines MFM Spec as the hosted MCP/database product using the MFM Spec format.
- Makes `mfm_spec_mutate` the normal authoring primitive, with `mfm_spec_write` reserved for
  import/bootstrap and escape-hatch whole-node replacement.
