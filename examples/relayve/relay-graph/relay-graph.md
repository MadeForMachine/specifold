---
id: relay-graph
title: Relay graph
parent: relayve
responsibility: Own canonical relay identity, versions, references, provenance classes, source attribution, and graph relationships.
tier: core
status: open
depends_on: [identity]
open_questions:
  - Should relay deletion be hard deletion only, or should public surfaces retain any tombstone later?
---

## Why

The relay graph is the load-bearing model of Relayve. Authored relays and
proxied relays must both behave as first-class relays so users can read,
reference, and branch from either kind without special discovery rules.

## Contract

Provides: relay identity, relay version history, current-version resolution,
editable authored references, provenance class, source attribution for proxied
relays, and graph deletion semantics. Consumes: user identity for authored relay
ownership only; it does not consume station publication state, Studio session
internals, or personal user context.

## Essential vs accidental

Essential: a relay has durable identity, versioned content, references to other
relays, and provenance that distinguishes user-authored relays from source-derived
proxied relays. Authored relays are owned by the creating user. Proxied relays
have system provenance and required source attribution instead of normal user
ownership. Accidental: the storage shape used to enforce this distinction.

## Rejected

Keeping proxied relays as feed-only summaries was rejected because it would split
the thought graph at the point external ideas enter Relayve. Modeling proxied
relays as if they belonged to a fake normal user was rejected because it would
leak system behavior into profiles, permissions, and publishing rules.
