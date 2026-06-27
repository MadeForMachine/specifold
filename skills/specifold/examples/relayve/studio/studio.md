---
id: studio
title: Studio
parent: relayve
responsibility: Manage private Ghosty sessions and create authored relays only when a session produces a finished thought.
tier: core
status: open
depends_on: [identity, relay-graph, agent-runtime]
open_questions:
  - How much session history should be retained after the authored relay is deleted?
---

## Why

Studio is the private workspace where authored relays are formed. It owns Ghosty
sessions, including sessions that do not produce a relay, because the working
conversation is private authoring state rather than part of the public relay
graph. Studio also receives Scoop handoffs when discovery turns into authoring.

## Contract

Provides: private Ghosty session lifecycle, session list state, Scoop handoff
acceptance, and relay creation only after a session produces a finished thought.
Consumes: authenticated user identity, and relay graph write operations through
Ghosty. (Scoop→Studio handoffs arrive as calls the tool-layer makes *into* Studio,
so the dependency runs tool-layer → Studio — being invoked is not a dependency.)

## Essential vs accidental

Essential: a user can start and resume Ghosty sessions, branch from an existing
relay into a new session, receive a Scoop handoff with selected relays and chat
context, and produce an authored relay only when the session has enough
meaningful substance. A completed authored relay has a one-to-one relationship
with the Ghosty chat that created it, and that chat is the creation log for the
relay even as the relay accumulates versions. Accidental: the session list
layout, editor controls, or exact readiness scoring mechanism.

## Rejected

Making Ghosty chats public by default was rejected for the MVP because the chat is
workshop material, not the finished thought. Relay drafts were rejected because
unfinished work remains a Ghosty session until a relay is generated.
