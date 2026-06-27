# Changelog — atlas

All notable changes to the Atlas skill. Entries marked **MAJOR** change the
skill's behaviour or the tools it depends on; plan to re-read the skill after a
major bump.

## 0.1.0 — 2026-06-27 (pre-release)
- Initial draft of the Atlas wayfinding skill: jump-don't-crawl, read-only-what-is-pinned,
  and typed absence (`mined-absent` vs `dark`).
- Renamed from `mfm-catalog` to `atlas` — Atlas is the engine's name, and the `mfm-` prefix
  is redundant inside the mfm namespace.
- Depends on the Atlas MCP tools (`atlas_capabilities`, `atlas_select`, `atlas_compare`,
  `atlas_provider`, `atlas_tree`) — now reconciled with the served MCP surface: these are the
  real read tools registered in `mcp/atlas_tools.py`, pass-throughs to the public `/v1/atlas`
  plane.
