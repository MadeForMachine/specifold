---
id: relayve
title: Relayve
parent: null
responsibility: Provide a platform for creating, publishing, discovering, and extending structured thought through a relay graph.
tier: core
status: open
depends_on: [identity, agent-runtime, relay-graph, studio, publishing, discovery, personal-context, proxy-publishing, administration]
open_questions:
  - Should the MVP expose public read paths before all authored workflows are complete?
---

## Why

Relayve is centered on structured thought rather than posts, notes, or generic
chat transcripts. The root component exists to keep the MVP organized around the
full loop: a thought is formed with agent help, represented as a relay, published
through stations, discovered in the feed, personalized by user context, and
extended into further relays.

## Contract

Provides: the top-level component map for the MVP and the boundary that keeps
creation, publishing, discovery, personalization, proxy publishing, and
administration aligned around the relay graph. Consumes: the responsibilities and
contracts of every direct child component. This spec currently contains only
MVP-core components; deferred or non-MVP concepts are intentionally excluded
rather than marked experimental.

## Essential vs accidental

Essential: Relayve must preserve a directed graph of thoughts and make it useful
to author, publish, discover, personalize, and branch from those thoughts.
Agents must act through explicit system capabilities rather than improvising
state changes. Accidental: the specific interface layout, data store, or AI
provider used to support that loop.

## Rejected

Treating Relayve as only a blogging tool was rejected because stations are a
publication surface, not the center of the system. Treating Relayve as only an AI
chat tool was rejected because the durable artifact is the relay graph, not the
conversation.
