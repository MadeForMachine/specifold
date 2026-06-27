---
id: station-follows
title: Station follows
parent: personal-context
responsibility: Let users manually follow stations as a discovery preference and agent context signal.
tier: core
status: open
depends_on: [personal-context, stations]
open_questions:
  - Should users also be able to mute stations separately from unfollowing them?
---

## Why

The feed will become noisy once user stations and proxy-operated stations both
publish relays. Following stations gives users a manual way to express which
channels matter to them and gives agents a clear preference signal.

## Contract

Provides: per-user followed-station state for feed filtering/context and agent
context. Consumes: followable station identity from Publishing and authenticated
user identity through Personal context.

## Essential vs accidental

Essential: users can manually follow and unfollow stations, and agents can read
follow state as context. Accidental: notification settings, mute state, station
recommendations, or agent-managed follows.

## Rejected

Making every published station equally important to the user was rejected because
proxy publishing can produce more content than a user wants in their working
context. Letting agents follow stations for the user was rejected for the MVP.
