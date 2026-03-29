# Infra


## Backend

### Database
- No need to use anything then a postgres database here.
It can easily handle 50k writes per minute which is the peak load.


### Promotions
- Creating promotional campaigns triggers a fan-out on write. We write a single record into the database with details about the campaign and its target audience.
- A job keeps polling the campaigns table and communicates with the notifications API to send notifications in small batches while keeping track of its progress through a column (`user_id_checkpoint`) 
- Once its done it flips the status column to indicate that.




## Notifications service

### Processing notifications
Here we'll have n workers that are process notifications based on a ratio that is calculated from their priority.
eg: It processes 10 jobs that are priority 8 or higher then it does 5 that are between 4 and 7 and 2 of anything lower, this enforces fairness.

### Retries
Workers poll `notification_deliveries` for rows with `status = 'pending'` or `status = 'failed'` where `retry_count` is below the configured maximum. To prevent two workers from picking up the same row, each worker uses `SELECT FOR UPDATE SKIP LOCKED` when claiming a delivery.

### Campaign fan-out concurrency
Each campaign is processed by a single job instance. If scaling is needed, a `worker_id` column can be added to `notification_campaigns` to act as a soft lock — a worker claims a campaign by writing its ID to that column before starting, preventing other instances from picking it up.
