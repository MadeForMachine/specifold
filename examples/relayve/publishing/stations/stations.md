---
id: stations
title: Stations
parent: publishing
responsibility: Represent user-owned and proxy-operated publication channels.
tier: core
status: open
depends_on: [publishing, identity, personal-context]
open_questions:
  - Should proxy source attribution be visible on every station listing or only on relay detail pages?
---

## Why

Stations are Relayve's publication channels: the product's version of blogs, but
connected to the relay graph. A station can be user-owned or proxy-operated, which
lets external channels enter Relayve through the same public concept as authored
publishing. Stations are also followable user-context objects.

## Contract

Provides: station identity, station ownership/operation mode, external source
identity for proxy-operated stations, public station metadata, and followable
station targets. Consumes: user identity for user-owned stations, proxy-publishing
configuration for proxy-operated stations, and personal context for follows.

## Essential vs accidental

Essential: a user may own one or more stations, a relay may be published on more
than one station, proxy-operated stations carry external source identity for
channels, podcasts, or blogs, and users can manually follow stations. Accidental:
domain routing, branding controls, station analytics, or agent-managed follows.

## Rejected

Creating a separate proxy station entity was rejected because proxy stations are
still stations. Hiding proxy stations inside source ingestion was rejected because
users should encounter proxied relays through the same publication model as other
relays.
