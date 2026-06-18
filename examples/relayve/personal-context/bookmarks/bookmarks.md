---
id: bookmarks
title: Bookmarks
parent: personal-context
responsibility: Let users manually save relays as a personal collection and preference signal.
tier: core
status: open
depends_on: [personal-context, relay-graph]
open_questions:
  - Should bookmarks later support user-authored notes or folders?
---

## Why

Bookmarks let users keep track of relays they care about. They also give Scoop and
Ghosty a high-signal view of the user's interests without requiring an inferred
preference model in the MVP.

## Contract

Provides: per-user saved relay state and a readable preference signal for agents.
Consumes: visible relay identity from the Relay graph and authenticated user
identity through Personal context.

## Essential vs accidental

Essential: users can manually bookmark and unbookmark visible relays, and agents
can read bookmark state as context. Accidental: collections, bookmark search,
notes, sharing, or automated bookmarking.

## Rejected

Treating bookmarks as relay references was rejected because bookmarks express a
user's interest, not thought lineage. Allowing agents to create bookmarks was
rejected for the MVP because the collection should reflect deliberate user action.
