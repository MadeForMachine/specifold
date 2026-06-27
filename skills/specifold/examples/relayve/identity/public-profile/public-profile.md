---
id: public-profile
title: Public profile
parent: identity
responsibility: Present a user's public description and links to their public stations.
tier: core
status: open
depends_on: [identity, stations]
open_questions:
  - Should public profiles list only stations, or also recent relays later?
---

## Why

Stations need an author context. A public profile gives readers a simple place to
understand who a user is and which stations they publish, without turning Identity
into a content owner.

## Contract

Provides: public user description and links to the user's public stations.
Consumes: public-safe user identity fields and station listings from Publishing.

## Essential vs accidental

Essential: users can maintain a public description, and readers can see links to
that user's stations. Accidental: follower counts, avatars, social links,
activity feeds, or profile customization.

## Rejected

Folding public profile behavior into stations was rejected because a user can own
multiple stations and needs one author-level entry point. Making profiles a
social network surface was rejected for the MVP.
