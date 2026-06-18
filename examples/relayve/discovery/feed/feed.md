---
id: feed
title: Feed
parent: discovery
responsibility: Present unique published relays ordered by newest publication while showing all stations where each relay appears.
tier: core
status: open
depends_on: [discovery, relay-graph, publishing, stations, personal-context, bookmarks, station-follows]
open_questions:
  - If one relay is published to multiple stations at different times, which publication date should control feed ordering?
---

## Why

The feed is the user's unified discovery stream. It should not care whether a
relay came from a user station or proxy-operated station, but it must avoid
showing duplicate entries when one relay is published in multiple places and must
carry enough user context to reflect bookmarks and followed stations.

## Contract

Provides: a deduplicated list of published relays, ordered by publication date,
with station links and current-user bookmark/follow context. Consumes: publication
state from Publishing, current relay versions from the Relay graph, station
metadata from Stations, and personal context from Bookmarks and Station follows.

## Essential vs accidental

Essential: the feed contains published relays, deduplicates by relay, orders by
publication date descending, displays links to every station where the relay is
published, and can expose bookmark/follow state for the current user. Accidental:
infinite scrolling, ranking, topic filters, or visual card design.

## Rejected

Letting each station publication appear as a separate feed item was rejected
because it would duplicate the same thought and make multi-station broadcasting
feel noisy.
