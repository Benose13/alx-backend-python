#!/usr/bin/python3
import seed


def stream_user_ages():
    """Generator to yield user ages one by one"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:   # loop 1
        yield row["age"]
    cursor.close()
    connection.close()


def compute_average_age():
    """Compute average age using the generator"""
    total = 0
    count = 0
    for age in stream_user_ages():   # loop 2
        total += age
        count += 1
    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")
