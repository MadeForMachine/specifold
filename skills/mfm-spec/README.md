# MFM Spec

MFM Spec is the hosted MadeForMachine product for service-backed MFM Specs. It stores
the canonical spec in the MFM service, exposes minimal-context reads and fine-grained
validated mutations through MCP, and keeps revision history in the service database.

Use `mfm-spec-local` for local file-backed specs. Use `mfm-spec` when the `mfm_spec_*`
MCP tools are available and the user wants a hosted, versioned spec memory.

## Install

MFM Spec Hosted needs two pieces:

- the `mfm-spec` skill, which teaches the agent the hosted authoring loop;
- the `mfm` MCP server, which exposes the authenticated `mfm_spec_*` tools.

The primary setup surface is [mfm.dev/mcp](https://mfm.dev/mcp). Install the skill from
[mfm.dev/skills/mfm-spec](https://mfm.dev/skills/mfm-spec), then connect and authenticate
the `mfm` MCP server.

Manual fallback:

```sh
git clone https://github.com/MadeForMachine/mfm-skills.git
cp -r mfm-skills/skills/mfm-spec ~/.claude/skills/mfm-spec     # Claude Code
cp -r mfm-skills/skills/mfm-spec ~/.agents/skills/mfm-spec     # Codex / Cursor
```

Then configure the MCP server at `https://mcp.mfm.dev/mcp` in your agent and complete
OAuth for the `mfm` server. If the `mfm_spec_*` tools are not visible after login,
start a fresh agent session so the tool list is refreshed.

## Status

Alpha and public for pilot setup. The hosted service is still hardening, but the skill
now names the real MCP surface implemented by the MadeForMachine service.
