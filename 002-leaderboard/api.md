# API Endpoints

## PUT /:playerId/score
> Updates a player's score

Updates to player score is done to both the **SQL Database** and **Redis**.
SQL: `UPDATE players SET score = score + <delta> WHERE id = <playerId>`
Redis: `ZADD leaderboard <playerId> <score_from_database_update>`

Here we have a dual write concern.
- We start by updating the score in the database and if that fails then the endpoint should error out.
- If the SQL update succeeded and Redis failed then we let it self heal in the next call to this endpoint. 

### Request
```
{ "delta": { "type": "integer" } }
```

### Response
204: Success

422: When delta is negative which is not allowed

404: User not found

500: Update failed

## GET /top-100
> Get the top 100 players

The top 100 can be easily fetched from redis with the following command
`ZREVRANGE leaderboard 0 99` which would return the list of user ids ranked by score which we then use to query the database for the player names and other metadata needed.


### Response
```json
{
    "data": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": { "type": "integer" },
                "score": { "type": "integer" }
            },
            "required": ["id", "score"],
        }
    }
}
```

## GET /rank
> Get authenticated user rank

Getting the user rank can also be easily done from **Redis** with the following command
`ZREVRANK leaderboard <playerId>`

### Response
```json
{
    "data": {
        "type": "object",
        "properties": {
            "id": { "type": "integer" },
            "score": { "type": "integer" },
            "rank": { "type": "integer" }
        },
        "required": ["id", "score", "rank"],
    }
}
```
