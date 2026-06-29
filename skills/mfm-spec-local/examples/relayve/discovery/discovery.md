---
id: discovery
title: Discovery
parent: relayve
responsibility: Let users read, find, discuss, and branch from published relays.
tier: core
status: open
depends_on: [relay-graph, publishing, studio, personal-context, agent-runtime]
open_questions: []
---

## Why

Discovery is the read and exploration side of Relayve. It connects published
relays back into authoring by making every discovered idea a possible starting
point for a new Ghosty session, and it uses manually managed personal context to
understand what the user cares about.

## Contract

Provides: read/discovery workflows over published relays, branching entry points
into Studio, and the boundary for Scoop's conversational discovery behavior.
Consumes: published relay availability from Publishing, relay content from the
Relay graph, personal context signals, and Studio handoff capability through the
Agent runtime.

## Essential vs accidental

Essential: users can read published relays, discover relays from user and proxy
stations, discuss feed content with Scoop, bookmark relays, follow stations, and
branch from a relay into Studio. Accidental: recommendation algorithms, saved
searches, personalization depth beyond manual signals, or social interactions.

## Rejected

Making discovery only a passive feed was rejected because Relayve's core loop is
extension: reading a relay should naturally lead to creating a new relay based on
it.
