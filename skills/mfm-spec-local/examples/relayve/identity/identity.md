---
id: identity
title: Identity
parent: relayve
responsibility: Represent authenticated users, public user profiles, and administrative authority without owning product content.
tier: core
status: open
depends_on: []
open_questions: []
---

## Why

Relayve needs users for authored relay ownership, private studio sessions,
station ownership, public author presence, personal context, and administration.
Identity is kept separate from product content so that authentication and
authority do not become the place where relay, station, or feed behavior hides.

## Contract

Provides: authenticated user identity, administrative authority, and public-safe
profile identity. Consumes: no product content ownership; other components use
Identity only to scope private work, assign authored ownership, check admin
authority, and present public author metadata.

## Essential vs accidental

Essential: authenticated users, user-scoped private work, public profile
identity, and an admin authority model. Accidental: provider-specific
implementation details, analytics, or organization support.

## Rejected

Owning relays through identity was rejected because relay provenance and graph
relationships belong in the relay graph. Organization ownership was rejected for
the MVP because single-user stations are sufficient and already match the
accepted auth direction.
