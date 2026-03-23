# API


## Single middleware that accepts the following parameters
```
{
    "group": { "type": "string" },
    "bucket_size": { "type": "integer" },
    "refill_rate_per_sec": { "type": "number" },
}
```
It also accepts a callback that returns a string which is used to identify the client.
```ts
app.use(rateLimit({
    group: 'timeline',
    bucket_size: 100,
    refill_rate_per_sec: 1,
    getIdentifier(ctx) {
        return ctx.user.id || ctx.request.ip_address;
    }
}))
```

The middleware would basically run lua script that handles the **Redis** state and rate limiting logic. The script would return one of the following:
1. `null` when the request should be let through
2. `{ "capacity": <bucket_size>, "remaining": <tokens_left>, "retry_after": <retry_after> }` where `retry_after` is only populated when the client has no more tokens left and it represents how many  seconds until the client's bucket receives one token.
