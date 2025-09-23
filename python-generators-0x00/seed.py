#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid

DB_NAME = "ALX_prodev"


def connect_db():
    """Connect to MySQL server (without selecting a database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # update with your MySQL username
            password="password"   # update with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None


def create_database(connection):
    """Create database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # update with your MySQL username
            password="password",  # update with your MySQL password
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to {DB_NAME}: {e}")
    return None


def create_table(connection):
    """Create user_data table if not exists."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            )
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Insert data from CSV file into user_data table."""
    try:
        cursor = connection.cursor()
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # check if email already exists
                cursor.execute("SELECT * FROM user_data WHERE email=%s", (email,))
                if cursor.fetchone():
                    continue

                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, name, email, age)
                )
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
