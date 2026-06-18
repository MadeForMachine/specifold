---
id: administration
title: Administration
parent: relayve
responsibility: Let admins manage proxy stations and operate source digestion.
tier: core
status: open
depends_on: [identity, stations, proxy-publishing, source-digestion]
open_questions: []
---

## Why

Administration is needed because proxy publishing is an internal Relayve
capability. Admins need a bounded way to configure proxy-operated stations and
control source digestion without exposing ingestion controls to regular users.

## Contract

Provides: admin-only management of proxy-operated stations and source-digestion
operations. Consumes: administrative identity, station management capabilities,
proxy-publishing controls, and source-digestion status.

## Essential vs accidental

Essential: admins can create and manage proxy-operated stations, attach external
source identity to those stations, and operate source digestion. Accidental:
general analytics, billing, moderation tooling, or broad platform settings.

## Rejected

Making administration a general back office was rejected for the MVP because it
would become a junk drawer. User-facing source ingestion was rejected because
regular users should only read, reference, and branch from proxied relays.
