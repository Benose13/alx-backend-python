#!/usr/bin/python3
import mysql.connector


def stream_users():
    """
    Generator that streams rows from user_data table one by one.
    Yields rows as dictionaries.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="Benose13",         
        password="Iamhead-11",     
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:   # only one loop
        yield row

    cursor.close()
    connection.close()
