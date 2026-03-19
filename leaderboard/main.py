import psycopg2
import random
import math


connection = psycopg2.connect(database='winter', user='winter')

total = 15_000_000
batch_size = 50_000
batch_count = math.ceil(total / batch_size)

for i in range(batch_count):
    scores = [random.randint(1, 1000000) for _ in range(batch_size)]

    values = ",".join([f"({score})" for score in scores])

    insert_query = f"INSERT INTO players (score) VALUES {values}"

    cursor = connection.cursor()
    cursor.execute(insert_query)
    connection.commit()
    print(f"Batch {i} done!")
