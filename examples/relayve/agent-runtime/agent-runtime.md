---
id: agent-runtime
title: Agent runtime
parent: relayve
responsibility: Run Relayve's AI agents through permissioned, traceable system capabilities.
tier: core
status: open
depends_on: [identity]
open_questions: []
---

## Why

Scoop and Ghosty need more than prompts. They need a shared runtime boundary that
decides what an agent may read, what it may change, how it hands work to another
component, and how each invocation is inspected after the fact.

## Contract

Provides: a common execution boundary for Scoop and Ghosty, a permission model for
agent capabilities, and traceability for agent invocations. Consumes:
authenticated user context from Identity and component capabilities exposed
through the Tool layer.

## Essential vs accidental

Essential: agents run as named actors with explicit permissions, call tools for
system actions, and leave internal traces for each invocation. Accidental: the AI
model loop implementation, streaming transport, retry mechanism, or provider.

## Rejected

Letting agents mutate Relayve by free-form prose was rejected because Scoop must
be able to reliably start a Ghosty session without gaining relay-writing powers.
Duplicating separate runtimes for Scoop and Ghosty was rejected because their
permission sets differ, but their execution and traceability needs are shared.
