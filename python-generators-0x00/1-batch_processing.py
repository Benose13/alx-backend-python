#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator to stream users from DB in batches"""
    connection = mysql.connector.connect(
        host="localhost",
        user="Benose13",
        password="Iamhead-11",  
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Process each batch to filter users over age 25"""
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user["age"] > 25:  # filtering, no loop
                print(user)
