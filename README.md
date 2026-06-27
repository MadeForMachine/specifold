# mfm-skills

> The public source of truth for [MadeForMachine](https://madeformachine.com) agent
> skills. Every public surface — the madeformachine.com skill pages, the mfm.dev
> machine pages, the install bundles — is **generated from this repo.**

A *skill* is a focused, procedural instruction set your coding agent loads to do
better work: it carries the opinion (how to approach a task), while the work itself
runs through tools — usually a MadeForMachine MCP connector. The skill is the
incision plan; the tools are the instruments; your agent holds the scalpel.

## Layout

One folder per skill under `skills/`. Each is self-contained:

```
skills/
  <name>/
    SKILL.md       # manifest frontmatter (see skill.schema.json) + the skill body
    CHANGELOG.md   # notable changes; entries marked MAJOR need a re-read
    …              # any assets the skill bundles (examples, scripts, reference linter)
skill.schema.json  # the frontmatter contract the page generator reads
```

The frontmatter is the keystone: `version`, `status`, `public`, `connector`,
`requires` (the MCP tool ids the body calls), and `license`. The generator turns
`frontmatter + body + CHANGELOG` into the public pages and the machine-readable JSON
twin — so the pages can't drift from the skill.

## Skills

| Skill | What it does | Status |
|-------|--------------|--------|
| [`specifold`](skills/specifold/) | Interrogates a system's architecture out of your head into a spec. | mvp |
| [`mfm-catalog`](skills/mfm-catalog/) | Steers your agent to traverse the MFM catalog — jump to doc evidence instead of crawling provider docs. | beta |

Internal / operator-scoped skills (e.g. the Atlas harvest tooling) are **not** in
this repo — they live in a private repo and are never published.

## Install

The primary, version-pinned install is the **mfm.dev page for each skill**
(`mfm.dev/skills/<name>`): hand it to your agent and it fetches the current version
and writes it to the right skills directory for your harness.

Manual install is the fallback — copy a skill folder into your agent's skills
directory:

```sh
git clone https://github.com/MadeForMachine/mfm-skills.git
cp -r mfm-skills/skills/specifold ~/.claude/skills/specifold     # Claude Code
cp -r mfm-skills/skills/specifold ~/.agents/skills/specifold     # Codex / Cursor
```

## License

[MIT](./LICENSE) — applies to every skill in this repo.
