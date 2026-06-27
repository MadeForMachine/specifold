# Specifold

> An agent-native specification format — and the skill that interrogates a
> system's architecture out of your head.
>
> Part of [MadeForMachine](https://madeformachine.com).

Working with a coding agent forces you to put your thinking in writing — and that
is where you discover how much of it was fuzzy. Specifold turns that moment into
the point of the exercise. It is an agent skill that takes a rough idea for a
software system and works with you to produce a clear architecture spec: a tree of
components, each with a single responsibility, its dependencies, and — the part
that usually evaporates — the reasoning behind why the system is shaped that way.

Its value is **not transcription, it is interrogation.** It hunts the fuzziness you
didn't mark, surfaces the boundary-deciding questions you'd have skipped, traces a
change across the whole system to catch the ripples you'd forget, and resists the
over-decomposition that turns architectures into sprawl. If it's just writing down
what you said, it's failing.

The result is the durable artifact. The conversation that produces it is
disposable, and so is any code generated from it later — the spec is the thing that
persists, in a format made to be read by both an agent and a human.

## What it does

- **Gets the theory out of your head.** You describe the system in your own words;
  it reflects back the *fewest* components that cover it and presses on what's
  vague, overlapping, or contradictory before writing anything.
- **Captures the *why*, not just the *what*.** Every component records its
  rationale, what's essential vs incidental, and the alternatives that were
  rejected — the tacit reasoning normally lost when a conversation ends.
- **Attends to the whole picture.** A new requirement rarely lands on one
  component; Specifold traces it across the tree and tells you exactly which
  components it touches, so you can check that it saw the whole.
- **Stays steerable.** Dial how hard it pushes ("challenge me", "push back
  harder"), navigate ("go deeper", "zoom out"), and finalize when you're ready.

## Scope: the architecture, and nothing below it

Specifold works at one level — the component tree. It deliberately does **not**
break components into detailed features, choose technologies or frameworks, or
generate code. Those are lower layers. Keeping this level free of them is what
keeps a spec small, portable across technology choices, and cheap to throw a new
idea at.

It is the first surface of a larger vision: a specification harness on which a team
can describe its entire infrastructure, from the broadest component down to the
finest detail. This is the top floor.

## What you get

One file per component, in a directory that mirrors the tree. Each carries a
machine-readable header an agent builds from and a prose body a human reads:

```markdown
---
id: routing-engine
title: Routing engine
parent: api-service
responsibility: Decide where each inbound item is delivered.
tier: core
status: open
depends_on: [identity, delivery]
open_questions:
  - sync or async dispatch?
  - retry policy on delivery failure?
---

## Why
Routing is its own component because delivery rules change far more often than
identity or transport — we want to change them without touching either.

## Rejected
Folding routing into a worker — it couples policy changes to infrastructure
changes, the entanglement that makes a system hard to evolve.
```

## Install

Specifold is an [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills).
The primary, version-pinned install is the **[mfm.dev/skills/specifold](https://mfm.dev/skills/specifold)**
page — hand it to your agent and it fetches the current version and writes it to the
right skills directory for your harness.

To install it manually instead, copy the `skills/specifold/` folder from this repo into
your agent's skills directory (`~/.claude/skills/specifold` for Claude Code, or the shared
`~/.agents/skills/specifold` for Codex and Cursor):

```sh
git clone https://github.com/MadeForMachine/mfm-skills.git
cp -r mfm-skills/skills/specifold ~/.claude/skills/specifold     # Claude Code
cp -r mfm-skills/skills/specifold ~/.agents/skills/specifold     # Codex / Cursor
```

Then just start describing a system you want to design — "help me architect…",
"get this idea out of my head", "map out the components" — or invoke it explicitly.

## The format

The specs Specifold produces conform to the **Specifold Format** — an open,
versioned, agent-native specification format. The current version is **v0.2** —
the architecture layer plus a feature layer. The normative definition — fields, body contract, integrity
rules, and a Pydantic reference schema — is in [`SPEC.md`](./SPEC.md), and it's
published in the open at [mfm.dev/specifold](https://mfm.dev/specifold).

The version number is a promise the format grows downward over time, not a claim
it's finished. `0.x` is unstable: fields may change between minor versions while
the format finds its shape, so every spec declares the version it was written
against.

## Status

Specifold is an early MVP, in pilot. We're recruiting teams to run it on real,
complex systems and tell us where it helps and where it breaks — that feedback
shapes what the harness becomes.

**[Join the pilot list →](https://madeformachine.com/skills/specifold)**

## License

[MIT](./LICENSE)
