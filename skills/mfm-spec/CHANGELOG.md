# Changelog — mfm-spec

## 0.2.0 — 2026-06-29
- Renames the hosted skill from `mrspec` to `mfm-spec`.
- Renames required MCP tools from `mrspec_*` to `mfm_spec_*`.
- Points local file-backed work to `mfm-spec-local`.

## 0.1.0 — 2026-06-29
- Initial alpha hosted-skill split from local MFM Spec.
- Defines MFM Spec as the hosted MCP/database product using the MFM Spec format.
- Makes `mfm_spec_mutate` the normal authoring primitive, with `mfm_spec_write` reserved for
  import/bootstrap and escape-hatch whole-node replacement.
