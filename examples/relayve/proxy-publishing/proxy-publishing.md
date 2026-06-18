---
id: proxy-publishing
title: Proxy publishing
parent: relayve
responsibility: Create immutable proxied relays from external sources and publish them to proxy-operated stations.
tier: core
status: open
depends_on: [relay-graph, publishing, stations]
open_questions: []
---

## Why

Proxy publishing brings external ideas into Relayve as first-class relays instead
of treating them as disposable summaries. This lets users discover, read, and
branch from external source material through the same relay graph used for
authored thoughts.

## Contract

Provides: system-created proxied relays and publication of those relays to their
matching proxy-operated stations. Consumes: proxy station source configuration,
source-digestion output, relay graph creation/versioning, and Publishing for
station placement.

## Essential vs accidental

Essential: proxy publishing creates source-derived relays with required source
attribution, no normal user ownership, no authored references in the MVP, and
publication only to the matching proxy-operated station. Proxied relays are not
editable by users, but users can use them as the base for authored relays.
Accidental: supported source formats, scheduling frequency, or summarization
implementation.

## Rejected

Letting users directly ingest arbitrary external content was rejected for the MVP
because source digestion is an internal/admin-operated capability. Allowing proxy
source attribution to be removed was rejected because a proxied relay without its
source becomes an unattributed AI summary.
