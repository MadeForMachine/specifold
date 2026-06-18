---
id: scoop
title: Scoop
parent: discovery
responsibility: Query and discuss feed content, then hand one or more relays and chat context into Ghosty as starting context.
tier: core
status: open
depends_on: [discovery, feed, studio, relay-graph, agent-runtime, tool-layer, agent-runs, personal-context, bookmarks, station-follows]
open_questions:
  - How explicit must the user's handoff request be before Scoop may start a Ghosty session?
---

## Why

Scoop is the conversational interface for discovery. It lets users query, filter,
and discuss feed content without turning discovery into a static list of posts.
When the user wants to turn a discovered idea into their own thought, Scoop hands
the selected relays and conversation context to Studio through a tool-layer
capability.

## Contract

Provides: conversational discovery over feed content and a controlled handoff into
Studio that starts a Ghosty session from selected relays plus chat context.
Consumes: feed/read tools, relay content, bookmarks, followed stations, agent-run
traceability, and the tool-layer permission that permits handoff but forbids
relay writing.

## Essential vs accidental

Essential: Scoop can reason over discoverable feed content, read manually managed
bookmarks and followed stations as preference context, help the user find
relevant relays, discuss them, and start a Ghosty session with one or more
selected relays plus chat context. Scoop cannot create or edit relays and cannot
bookmark or follow on the user's behalf in the MVP. Accidental: the chat UI
layout, memory depth, or exact query language.

## Rejected

Merging Scoop with Ghosty was rejected because Scoop discovers and interprets
published relays, while Ghosty helps author new ones. They may share underlying AI
capabilities, but their product responsibilities are different.
