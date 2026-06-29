# Changelog — mfm-spec-local

All notable changes to the MFM Spec local skill. Entries marked **MAJOR** change the
skill's behaviour or the MFM Spec format it targets; plan to re-read the skill
after a major bump. The skill version tracks the skill itself; the MFM Spec
Format version it targets is noted per release.

## 0.6.0 — 2026-06-29
**MAJOR.** Renames the local skill from `specifold` to `mfm-spec-local`.
- Keeps **MFM Spec** as the single product/format name.
- Uses `mfm-spec.yaml`, `mfm-spec.schema.json`, and `mfm_spec_lint.py` for the local file format bundle.
- Points hosted service-backed work to the separate `mfm-spec` skill.

## 0.5.0 — 2026-06-29
**MAJOR.** Splits hosted service authoring out of MFM Spec.
- MFM Spec is now local-file-backed only: node files plus `mfm-spec.yaml` in the user's
  project, validated by the bundled linter.
- Git is optional, not a source-of-truth assumption.
- The hosted MCP/database mode is now **MFM Spec** and lives in its own skill.

## 0.4.0 — 2026-06-29
**MAJOR.** Targets MFM Spec format **v0.3** and moves the skill from
component-only authoring to MVP graph authoring.
- Adds `evaluation` nodes as the minimal durable feedback record: subject, verdict,
  summary, evidence, promoted lessons, and rejected ideas.
- The skill now classifies raw user input into components, features, evaluations,
  open questions, and lower-layer details before shaping the spec.
- Updates the bundled linter and schemas to understand v0.3 while keeping v0.1/v0.2
  specs readable.

## 0.3.0 — 2026-06-27
**MAJOR.** Dual-backend persistence — one skill, two places a spec can live.
- The interrogation brain is unchanged; only the **persistence tail** forks. The
  backend is an explicit up-front choice (*"local files or the MFM service?"*), never
  inferred from whether the MFM connector is configured.
- **Local mode** is the existing behaviour: node files, the reference linter, git.
- **Service mode** reads and writes the canonical server-stored spec through the
  MadeForMachine MCP tools (`spec_read` / `spec_write`), validated server-side by
  `spec-core` — the same rules as the local linter, so consistency can't drift
  between backends. Covers the `base_rev` conflict and server-side validation loop.

## 0.2.0 — 2026-06-27
**MAJOR.** Targets MFM Spec format **v0.2** (architecture layer + feature layer).
- Skill now lives in the `mfm-skills` repo at `skills/mfm-spec-local/` (was its own repo).
- Primary install is the version-pinned [mfm.dev/skills/mfm-spec-local](https://mfm.dev/skills/mfm-spec-local)
  page; manual clone of `mfm-skills` is the fallback.
- Carries manifest frontmatter (`version`, `status`, `public`, `connector`, `requires`, `license`).

## 0.1.0
- Initial pilot release: architecture-layer interrogation with the bundled reference
  linter (`mfm_spec_lint.py`) and the open MFM Spec format definition (`SPEC.md`).
