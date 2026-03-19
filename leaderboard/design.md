# Design

## Infra

### Problem
- The whole API revolves around keeping track of player scores and ranking them based on that.
- Using a standalone on-disk database here will not scale very well because we need to handle a high number of reads/updates.
- There's also no efficient way to get the rank of a player even with an index.

### Solution
- A **Redis** instance on top of our database to handle the high rate of reads/writes.
- **Redis sorted sets** are designed for this exact use case. They're very good at associating keys with scores and ranking them based on their score.
- The **SQL database** should only be used for writes and recovery in case Redis goes down.
- Score updates should go to both **Redis** and the **SQL Database**
- Player ids would be used as keys.
- Fetching a player's rank can be easily done with the `ZREVRANK` **Redis** command
- Getting the top/bottom players by score can be easily done with `ZREVRANGE`/`ZRANGE`
- Updates to scores can be done with `ZADD`.
- 

## Requirements
> Handling 1,000 score updates per second without the leaderboard reads becoming slow
- Writes go both to **Redis** and the **SQL Database** both can handle this number of writes without issues.
- Reads won't be affected since we're using sorted sets which are pretty efficient for this use case and **Redis** can easily handle a high number of reads/writes easily since it's in-memory.
    - `ZADD` has a time complexity of `O(log(N))`
    - `ZREVRANGE` has a time complexity of `O(log(N)+M)` with `M` being the number of elements returned.
