---
id: ghosty-authoring
title: Ghosty authoring
parent: studio
responsibility: Conduct authoring conversations, surface relevant relays, and produce or regenerate relay versions with references.
tier: core
status: open
depends_on: [studio, relay-graph, agent-runtime, tool-layer, agent-runs, personal-context, bookmarks, station-follows]
open_questions:
  - What minimum author contribution should be required before Ghosty can generate a relay?
---

## Why

Ghosty is not just a text generator; it is the authoring partner that helps the
user express a structured thought. It also connects the current discussion to the
existing relay graph by surfacing relays that may shape the new thought and by
reading manually managed personal context as preference signal.

## Contract

Provides: authoring conversation behavior, relay generation readiness, authored
relay creation, relay version regeneration, derived TLDR/reader-prompt generation,
and reference proposals. Consumes: Studio sessions, Scoop handoff context, relay
read/write tools, bookmarks, followed stations, and agent-run traceability.

## Essential vs accidental

Essential: Ghosty conducts the private conversation, accepts relay/chat context
from Scoop handoffs, reads bookmarks and followed stations as user preference
context, decides when a relay can be generated, generates the relay fields,
regenerates TLDR and reader prompt when content changes, and proposes references
when prior relay content materially flows into the result. Accidental: prompt
wording, model choice, and the exact retrieval method used to find relevant
relays.

## Rejected

Allowing one-click relay generation from an empty prompt was rejected because the
MVP requires the user to express something meaningful before a relay exists.
Treating suggested references as immutable citations was rejected because Relayve
is not a scientific publishing platform and authored references are editorial.
