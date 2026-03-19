# Exercise 3: Paste Bin (pastebin.com)

## Question

Design a paste bin service where users can share text snippets.

## Requirements

- Users can submit text and get back a unique URL to share
- Pastes can be public or unlisted (accessible only via URL)
- Pastes can optionally expire after a user-specified duration
- Users can view the raw text or a syntax-highlighted version
- The system should handle pastes up to 10MB in size

## Deliverables

1. Database schema (tables, columns, types, indexes)
2. API endpoints (method, path, request/response bodies)
3. One paragraph explaining how you'd handle storage efficiently when the system has 50 million pastes
