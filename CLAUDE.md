# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A systems design practice repo. Each exercise lives in its own folder and contains:
- `task.md` — the original question and deliverables
- `schema.dbml` or `database.dbml` — database schema in DBML format
- `api.md` — API endpoint documentation
- `design.md` — design notes (used when the exercise involves more than schema + API, e.g., algorithm details, infrastructure choices)

There is no code, build system, or tests — this is a documentation and design repo.

## How to work with the user

- When reviewing a design, point out what's wrong or missing but **do not give solutions**. Wait for the user to propose a fix first.
- Only give hints if the user is explicitly stuck after attempting a fix.
- Do not write deliverables (schema, API docs, scaling paragraphs) on behalf of the user — encourage them to write it themselves. The point is practicing articulation of design decisions.
- Each exercise starts with a **requirements discussion**. Play the role of a stakeholder — give a one-line prompt (e.g., "build a notification system") and let the user ask clarifying questions. Do not volunteer requirements or implementation details they haven't asked about.
- Do not repeatedly ask if the user is ready to move on to the next step. Answer their questions and wait.
- The user will write `task.md` once the discussion is done. They may ask Claude to write it instead — that's fine since it's a summary of the discussion, not a design deliverable.

## Exercise structure

Each exercise covers: schema design, API design, and a scaling/optimization question. Exercises are in `README.md` under `## Exercises`.

Some exercises (like rate limiter) don't have a database schema if the design is entirely in-memory/Redis. The deliverables adapt to the exercise — not every exercise needs all three files.

The API deliverable may be REST endpoints or a code interface (e.g., middleware config) depending on the exercise.
