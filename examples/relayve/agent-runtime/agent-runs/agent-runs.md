---
id: agent-runs
title: Agent runs
parent: agent-runtime
responsibility: Persist each agent invocation's input, tool calls, output, status, and errors.
tier: core
status: open
depends_on: [agent-runtime, identity, tool-layer]
open_questions:
  - How much of an agent run trace should ever be visible to end users?
---

## Why

Relayve depends on AI agents for core workflows. When an agent fails, makes a bad
handoff, or produces unexpected output, the system needs a record of what was
asked, which tools were called, what came back, and how the run ended.

## Contract

Provides: internal run records for Scoop and Ghosty invocations, including input,
tool-call trace, output, status, timing, and errors. Consumes: agent identity,
user identity, and tool-call events from the Agent runtime.

## Essential vs accidental

Essential: every Scoop and Ghosty invocation leaves an internal trace. Agent runs
are operational/audit records, not the public creation log of a relay. Accidental:
cost accounting, retention policy, trace viewer UI, or streaming details.

## Rejected

Using the Ghosty chat as the only debugging artifact was rejected because Scoop
also runs, tools can fail outside the chat transcript, and operational traces
serve a different purpose than the user's creation log.
