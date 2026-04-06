# ADR 0002: Data Model Decisions

## Status

Accepted

## Context

Data model design choices affect how the implementation agent builds the
persistence layer. Making these explicit prevents guesswork.

## Decisions

- **Tea.type** is a closed enum (green, black, oolong, white, puerh, herbal, other)
- **Tea.freshness_status** is computed on read, not stored
- **Tea** has a unique constraint on user_id, name, vendor
- **User** has a unique constraint on email

## Consequences

The data model is explicit and implementation-ready. The agent doesn't need
to infer types, constraints, or computation strategies.
