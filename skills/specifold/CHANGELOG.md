# Changelog — specifold

All notable changes to the Specifold skill. Entries marked **MAJOR** change the
skill's behaviour or the Specifold Format it targets; plan to re-read the skill
after a major bump. The skill version tracks the skill itself; the Specifold
Format version it targets is noted per release.

## 0.5.0 — 2026-06-29
**MAJOR.** Splits hosted service authoring out of Specifold.
- Specifold is now local-file-backed only: node files plus `specifold.yaml` in the user's
  project, validated by the bundled linter.
- Git is optional, not a source-of-truth assumption.
- The hosted MCP/database product is now **MrSpec** and lives in its own skill.

## 0.4.0 — 2026-06-29
**MAJOR.** Targets Specifold Format **v0.3** and moves the skill from
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
**MAJOR.** Targets Specifold Format **v0.2** (architecture layer + feature layer).
- Skill now lives in the `mfm-skills` repo at `skills/specifold/` (was its own repo).
- Primary install is the version-pinned [mfm.dev/skills/specifold](https://mfm.dev/skills/specifold)
  page; manual clone of `mfm-skills` is the fallback.
- Carries manifest frontmatter (`version`, `status`, `public`, `connector`, `requires`, `license`).

## 0.1.0
- Initial pilot release: architecture-layer interrogation with the bundled reference
  linter (`specifold_lint.py`) and the open Specifold Format definition (`SPEC.md`).
