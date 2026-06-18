---
id: publishing
title: Publishing
parent: relayve
responsibility: Publish relays to stations and resolve publications to each relay's latest version.
tier: core
status: open
depends_on: [identity, relay-graph]
open_questions:
  - Should publication date update when a relay receives a new version?
---

## Why

Publishing turns relays into publicly readable station entries. It is separate
from the relay graph because a relay's thought identity and a station's public
placement are different concerns.

## Contract

Provides: relay publication state, multi-station broadcast, and latest-version
resolution for public station entries. Consumes: relay identity/current-version
state from the Relay graph, user identity for publication authority, and station
identity from Stations.

## Essential vs accidental

Essential: user-owned relays can be broadcast to one or more user-owned stations,
proxied relays can be published only through proxy-operated stations, and all
publications resolve to the latest relay version. Accidental: scheduling, custom
domains, analytics, or rich editorial workflows.

## Rejected

Embedding station membership directly in relay identity was rejected because the
same relay can appear on multiple stations. Pinning a publication to a specific
relay version was rejected for the MVP because it adds release management before
the product needs it.
