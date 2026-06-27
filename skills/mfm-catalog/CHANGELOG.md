# Changelog — mfm-catalog

All notable changes to the catalog skill. Entries marked **MAJOR** change the
skill's behaviour or the tools it depends on; plan to re-read the skill after a
major bump.

## 0.1.0 — 2026-06-27 (pre-release)
- Initial draft of the catalog wayfinding skill: jump-don't-crawl, read-only-what-is-pinned,
  and typed absence (`mined-absent` vs `dark`).
- Depends on the MFM MCP catalog tools (`mfm_capabilities`, `mfm_select`, `mfm_compare`,
  `mfm_provider`, `mfm_tree`). **These tool names are not yet final** — they must be
  reconciled with the served MCP surface before this ships.
