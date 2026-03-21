# Exercise 2: Leaderboard

## Question

Design a leaderboard system for a mobile game.

## Requirements

- Players have a score that can be updated at any time
- Users can query the top 100 players globally
- Users can query their own rank (e.g. "you are #4,231 out of 10,000,000 players")
- Scores only go up (no deductions)

## Deliverables

1. Database schema (tables, columns, types, indexes)
2. API endpoints (method, path, request/response bodies)
3. One paragraph explaining how you'd handle 1,000 score updates per second without the leaderboard reads becoming slow
