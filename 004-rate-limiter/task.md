# Exercise 4: Rate limiter

## Question

Design a rate limiter

## Requirements

- Rate limit authenticated users by user ID, fall back to IP for unauthenticated users
- Token bucket algorithm: 30 tokens per minute
- Allow short bursts of traffic without penalizing normal usage
- Support configurable rate limit groups — a key can represent a single route, a route group, or an entire app
- Return a clear response when a request is rate limited, including when the client can retry
- Scale: ~10 million registered users, ~500k concurrent users at peak

## Deliverables

1. **Schema** — data model for tracking request counts (`schema.dbml`)
2. **API** — rate limiter interface and HTTP response behavior (`api.md`)
3. **Scaling** — how would you handle this at 500k concurrent users at peak?
