# Changelog — specifold

All notable changes to the Specifold skill. Entries marked **MAJOR** change the
skill's behaviour or the Specifold Format it targets; plan to re-read the skill
after a major bump. The skill version tracks the skill itself; the Specifold
Format version it targets is noted per release.

## 0.2.0 — 2026-06-27
**MAJOR.** Targets Specifold Format **v0.2** (architecture layer + feature layer).
- Skill now lives in the `mfm-skills` repo at `skills/specifold/` (was its own repo).
- Primary install is the version-pinned [mfm.dev/skills/specifold](https://mfm.dev/skills/specifold)
  page; manual clone of `mfm-skills` is the fallback.
- Carries manifest frontmatter (`version`, `status`, `public`, `connector`, `requires`, `license`).

## 0.1.0
- Initial pilot release: architecture-layer interrogation with the bundled reference
  linter (`specifold_lint.py`) and the open Specifold Format definition (`SPEC.md`).
