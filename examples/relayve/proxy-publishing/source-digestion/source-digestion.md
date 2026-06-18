---
id: source-digestion
title: Source digestion
parent: proxy-publishing
responsibility: Check external sources configured by proxy stations and transform new source items into proxied relay content.
tier: core
status: open
depends_on: [proxy-publishing, stations, relay-graph]
open_questions:
  - Which source item identity is sufficient to prevent duplicate proxied relays?
---

## Why

Source digestion is the internal process that turns new external content into
Relayve-native thought artifacts. It is named separately from the feed because
reading content and transforming external sources are different responsibilities.

## Contract

Provides: normalized source items suitable for proxied relay creation, including
source identity, source URL, extracted core content, and duplicate-detection
inputs. Consumes: configured proxy station source identity and external source
content.

## Essential vs accidental

Essential: source digestion checks configured proxy station sources, detects new
source items, extracts their core ideas, creates immutable proxied relay fields,
and preserves a link to the original source. Accidental: polling intervals,
transcription mechanics, media-specific extraction details, or retry
infrastructure.

## Rejected

Putting source digestion inside the feed was rejected because the feed should only
present published relays. Making source digestion user-accessible was rejected for
the MVP because proxy publishing is operated by admins.
