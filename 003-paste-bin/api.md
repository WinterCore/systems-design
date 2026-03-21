# API Endpoints

## POST /
> Create a new paste

Creating new pastes is straight forward:
- We generate an ID using a snowflake algorithm to be stored in the `id` column.
- We base62 encode the generated id to make it short for URL usage to be stored in the `short_id` column.
- We generate an **s3** presigned URL with a 10mb limit which the user can use to upload the contents of the paste.
- An **s3** event listener on the backend checks for new uploads and flips the uploaded flag to true.

### Request
```json
{
    "visibility": {
        "type": "string"
        "enum": ["public", "private"],
        "default": "private"
    },
    "language": {
        "type": "string",
        "enum": ["text", "javascript", "python"],
        "default": "text"
    },
    "title": { "type": "string" },
    "content_snippet": { "type": "string" },
    "expires_at": {
        "type": "string",
        "format": "date-time"
    },
}
```
### Response
201: Paste is created and its ID is returned
```json
{ "id": { "type": "string" }, "presigned_upload_url": { "type": "string" } }
```

422: Content too big or validation error

## GET /{id}
> Get a paste by ID

We use the ID to query the paste from the database, taking into account the `uploaded` and the `expires_at` columns. If `expires_at` not null and paste expired then we delete it and return 404.

We return the title, language and created_at columns and let the frontend handle getting the content from **s3** by using the ID.

### Request
Empty

### Response
200:
```json
{
    "title": { "type": "string" },
    "language": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
}
```
404: Paste not found


## GET /pastes
> Get the most recent pastes

This returns the most recent pastes and supports pagination.
Queries the database with `WHERE visibility = 'public' AND uploaded is true AND (expires_at is null OR expires_at > now()) AND id > <after_id> ORDER BY id DESC`
It returns the title, the creation date, the language and the `content_snippet`.
Pagination can be done with range queries on the `id` column since it's a snowflake

### Query
```json
{
    "after_id": { "type": "integer" },
}
```

### Response

```json
{
    "id": { "type": "string" },
    "title": { "type": "string" },
    "language": { "type": "string" },
    "content_snippet": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
}
```
