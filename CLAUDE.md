# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A systems design practice repo. Each exercise lives in its own folder and contains:
- `task.md` — the original question and deliverables
- `schema.dbml` — database schema in DBML format
- `api.md` — API endpoint documentation

There is no code, build system, or tests — this is a documentation and design repo.

## How to work with the user

- When reviewing a design, point out what's wrong or missing but **do not give solutions**. Wait for the user to propose a fix first.
- Only give hints if the user is explicitly stuck after attempting a fix.
- Do not write deliverables (schema, API docs, scaling paragraphs) on behalf of the user — encourage them to write it themselves. The point is practicing articulation of design decisions.

## Exercise structure

Each exercise covers: schema design, API design, and a scaling/optimization question. Exercises are in `README.md` under `## Exercises`.
