# Exercise 5: Notification System

## Question

Design a notification system for an e-commerce platform.

## Requirements

- Notify users about: order updates (confirmed, shipped, out for delivery, delivered), wishlist price drops, promotional campaigns
- Notify sellers about: new orders, product reviews
- Delivery channels: in-app notification center, push notifications (mobile), email (order updates only)
- Notification center in the app where users can view all past notifications and mark them as read
- Users can manage notification preferences — opt in/out per notification type and per channel
- Order update notifications are mandatory and cannot be opted out of
- Priority levels: order updates (highest), price drops, promotions (lowest)
- Retry failed push notification and email deliveries
- Scale: ~20 million registered users, ~2 million daily active users
- Peak load: ~50,000 notifications per minute (e.g., Black Friday), normal: ~5,000 per minute

## Deliverables

1. **Schema** — data model for notifications, user preferences, and delivery tracking (`schema.dbml`)
2. **API** — endpoints for notification center, preferences, and sending notifications (`api.md`)
3. **Scaling** — how would you handle peak load of 50k notifications per minute?
