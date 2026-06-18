---
id: tool-layer
title: Tool layer
parent: agent-runtime
responsibility: Expose stable callable product capabilities to agents and UI with explicit permissions.
tier: core
status: open
depends_on: [agent-runtime, identity, relay-graph, studio, publishing, discovery, personal-context]
open_questions:
  - Which user actions require explicit UI confirmation before a tool may execute them?
---

## Why

Scoop needs to hand discovered ideas into Studio without pretending to be Ghosty,
and Ghosty needs to write relay versions without receiving unrelated discovery or
administration powers. A tool layer turns those boundaries into callable
contracts.

## Contract

Provides: read tools for relays, feed, bookmarks, and followed stations; a Scoop
handoff tool that starts a Ghosty session from selected relays and chat context;
Ghosty-only write tools for creating relays from sessions, regenerating relay
versions, and updating relay references; UI-only tools for manual bookmarking,
unbookmarking, following, unfollowing, and profile editing. Consumes: user
identity, relay graph operations, Studio session creation, publishing/station
state, discovery queries, and personal context.

## Essential vs accidental

Essential: Scoop can read discovery context and start a Ghosty session, but cannot
create or edit relays. Ghosty can read discovery and personal context and can
write authored relays through Studio-controlled creation. Agents may observe
bookmarks and followed stations in the MVP, but may not modify them. Accidental:
transport shape, schema library, in-process versus network execution, or exact
tool names.

## Rejected

Allowing Scoop to create relays directly was rejected because it collapses the
discovery and authoring boundary. Allowing agents to bookmark or follow on the
user's behalf was rejected for the MVP because personal context should be
manually controlled until agent-initiated user actions have stronger consent
rules.
