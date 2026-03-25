# Notifications Service API

## POST /
> Create a new notification

Simple endpoint that takes in the request data and populates the `notifications` and `notification_deliveries` tables.

### Request
```json
{
    "type": "object",
    "properties": {
        "title": { "type": "string" },
        "content": { "type": "string" },
        "priority": { "type": "integer" },
        "user_id": { "type": "integer" },
        "channels": {
            "type": "array",
            "items": {
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": { "const": "email" },
                            "email": { "type": "string" },
                        },
                        "required": ["type", "email"]
                    },
                    {
                        "type": "object",
                        "properties": {
                            "type": { "const": "push" },
                            "token": { "type": "string" },
                        },
                        "required": ["type", "token"]
                    }
                ]
            }
        }
    },
    "required": ["title", "content", "priority", "user_id", "channels"],
}
```

### Response
- 201: Success
- 422: Invalid request: email or push notification token are invalid


## GET /
> Get paginated notifications of a user sorted DESC by time

```sql
SELECT * FROM notifications
WHERE user_id = <user_id>
AND id < <after_id>
ORDER BY created_at DESC
LIMIT <page_size>
```

Note: The page size has a default and an upper limit enforced by the code

### Query
```json
{
    "type": "object",
    "properties": {
        "after_id": { "type": "integer" },
        "user_id": { "type": "integer" },
        "page_size": { "type": "integer", "maximum": 50, "minimum": 5 },
    },
    "required": ["user_id"]
}
```

### Response
- 200:
  ```json
  {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": { "type": "integer" },
            "title": { "type": "string" },
            "content": { "type": "string" },
            "is_read": { "type": "boolean" },
            "created_at": { "type": "string", "format": "date-time" },
        },
        "required": ["id", "title", "content", "is_read", "created_at"]
    }
  }
  ```

## PUT /read_status
> Toggle read status of one or more notifications

```sql
UPDATE notifications
SET is_read = <is_read>
WHERE ids in <ids>
```

### Request
```json
{
    "type": "object",
    "properties": {
        "ids": {
            "type": "array",
            "items": { "type": "integer" }
        },
        "status": {
            "type": "string",
            "enum": ["read", "unread"]
        }

    },
    "required": ["ids", "status"]
}
```

### Response
- 200: Updated successfully!


# Backend API

## 
