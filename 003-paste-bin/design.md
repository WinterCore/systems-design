## Infra

### Storage
- S3 is a good choice because we're dealing with big pastes (up to 10mb) and a large number of them. Keeping this data in a single database will run us into limits in the future and make things possibly slow.
- Files will be named with an ID that will be generated upon creation which will be stored in the **SQL** database to reference the file later.

### ID Generation
- We should use some snowflake algorithm and base62 encode the ID to make it short and store both in the database.

### Database
- **Postgres** should be used for keeping track of created pastes. 
- We store a snippet of the content which the user provides when calling the API endpoint.
- Once the user uploads the content file. The file created **s3** event listener on the backend would flip the `uploaded` column of the paste to true to make it accessible.

#### Dealing with expired pastes
- We can have a job that runs periodically that cleans up records that have expired but were not deleted (since we delete on access) and not uploaded pastes.

### Requirements
> One paragraph explaining how you'd handle storage efficiently when the system has 50 million pastes
- **Postgres** can easily handle 50 million records without issues.
- Accessing pastes will be mostly done by ID which is pretty fast since the ID column is indexed by virtue of being a primary key.
- Listing recent public pastes is also fast because we can use the snowflake `id` with range queries.
- We have frontend fetch the contents of pastes from **s3** directly to keep the backend efficient, fast and reduce bandwidth.
- We can have the frontend also upload the contents of the paste to **s3** directly with a presigned URL to avoid having to go through the backend. This has one downside though in that we have to rely on the user to provide the snippet through the create paste API which they may choose to provide something completely different which is not a big deal IMO.
