## Infra

### Rate limit algorithm
The **Token Bucket** algorithm is chosen here because it's the most practical for this use case and easiest to implement.

### State
**Redis** will be used to store the rate limit state per client per group.

- We can just use **Redis** strings and the `SET`/`GET` commands to deal with state. 
- The **Token Bucket** algorithm requires storing the timestamp of the most recent request and the number of tokens left per identifier.
- An identifier here could be the **IP address** for unauthenticated clients or the database **User ID** for authenticated clients.
- We'll also use a group prefix which allows us to have different rate limit configs for different services/routes/servers.
- The **key format** based on all of the above is `rate-limiter:<group_str>:<client_identifier>`.

### Logic
- The rate limiter requires 3 parameters:
    - The group key
    - The token cap (maximum number of tokens the bucket can hold)
    - The refill rate (n tokens per sec)
- When a new request comes in, we calculate its key and try to get the existing rate limit value for it. Here we have two possible cases:
    - It doesn't exist: We set its value to `<timestamp>:<tokens_left>` where timestamp is the time of the request and tokens_left is the token cap. Finally we let the request through.
    - It exists: We refill the tokens by getting the delta between the timestamp of the current request and the stored timestamp to calculate how many tokens we should refill and multiply it by the refill rate capped by token cap. So basically `tokens_left = min((request_timestamp_seconds - timestamp_seconds) * token_refill_rate + tokens_left, token_cap)`
      Here, if the refilled (updated) tokens left ends up as 0, we drop the request and do nothing. Otherwise, we update the value of the key to `<current_request_timestamp>:<new_tokens_left>` where current_request_timestamp is the timestamp of the current request and new_tokens_left is the the tokens_left we got from the formula above minus 1 for the current request, and we let the request through.
    - All stored values should have a TTL of how much time it takes to refill the bucket up to token cap based on the provided refill rate. eg: if the refill rate is 0.5 token per second and the cap is 90 then the TTL should be 180 seconds.
- To guarantee atomicity for when getting the existing number of tokens left and calculating the new number we can use `EVAL` and do the entire calcluation in a lua script.


### Requirements
> Dealing with 500k concurrent users at peak.
The only problem that we may run into is running out of memory here. Let's say that the maximum key length is 24 characters long which is 24 bytes, and in the value we're storing the timestamp which is around 14 characters plus the separator plus 2-3 characters for the limit. Total is around 40 bytes. 40*500k is around 20MBs which is nothing.

