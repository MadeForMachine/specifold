---
id: personal-context
title: Personal context
parent: relayve
responsibility: Own manually managed user signals that shape discovery and agent context without changing relay or station ownership.
tier: core
status: open
depends_on: [identity, relay-graph, publishing]
open_questions: []
---

## Why

Relayve needs a place for user-specific preference signals that are not part of
the public relay graph. Bookmarks and followed stations help the user collect
important relays and shape what Scoop and Ghosty understand about their interests.

## Contract

Provides: user-specific bookmark and station-follow state for discovery and agent
context. Consumes: authenticated user identity, readable relays, and followable
stations.

## Essential vs accidental

Essential: personal context is manually managed by the user in the MVP and can be
read by Scoop and Ghosty as preference context. Accidental: recommendation
ranking, folders, labels, inferred interests, or agent-managed personalization.

## Rejected

Putting bookmarks or follows on relays and stations themselves was rejected
because they are per-user signals, not content ownership or publication facts.
Letting agents mutate personal context was rejected for the MVP to keep user
preference state explicit.
