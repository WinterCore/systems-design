# API Endpoints

## POST /
> Create new short URL

ID generation can be done by using some sort of snowflake algorithm that incorporates a timestamp, a server id and a sequence number which then we can base62 encode to end up with a short id.

### Request
```
{
    "url": { "type": "string" },
    "expires_at": {
        "type": "string",
        "format": "date-time"
    }
}
```
### Response
201
```
{ "short_url": { "type": "string" } }
```

422: Validation error, url is malformed or expires_at is in the past

## GET /{id}
> Get short URL aka **Visit** the URL

It does a lookup in the in-memory cache first before checking the database
This basically does a lookup in the database for a record matching the id from the params
`SELECT * FROM short_urls WHERE short_url_id = '<id>'`

Expiry can be implemented in one of two ways.
1. We can add `AND expires_at > now()` to the query and just keep expired records in the database, this has the advantage that clicks are always accessable since we keep the record in the database.
2. We fetch the record and check whether it's expired in the backend code, if it's we delete the record and return 404

Incrementing the visit count can be done with the following query
`UPDATE short_urls SET clicks = clicks + 1 WHERE short_url_id = '<id>'`

### Response
302: Redirects to long URL
**why:** 302 over 301 because we don't want links to be cached in browsers and possibly still redirect even after they're expired

404: Link not found

## GET /{id}/info
200
```
{
    "visits": { "type": "integer" },
    "expires_at": {
        "type": "string",
        "format": "date-time"
    },
}
```

404: Link not found


# Optimizations
## Caching links and buffering count writes
We can use an in-memory database and write every new link to it with a TTL, every time the link is accessed we basically increase the TTL but also keep in mind that we don't let it live beyond the expires_at. We can do a `MIN(expires_at, now() + 60s)` for example
For tracking click count, we only care about the approximate number of clicks, so we can also store these in the in-memory cache and flush when either a time limit is reached or a certain clicks delta whichever comes first

## Handling 10k clicks per second
Here the problem isn't with efficiently accessing the link but with initializing the cache for the first time.
If we have a link that's not already in the cache and suddenly we receive 10k requests for it at once we end up with a thundering herd problem.
Every one of these requests will get a cache miss and try to fetch the record from the database and cache it which is extremely inefficient.
To solve this we can put a lock on the unique id of the link which one of these requests can acquire and be responsible for putting its data in the cache, while the other requests wait until the data is cached before they complete.
