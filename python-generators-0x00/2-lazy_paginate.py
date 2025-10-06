#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    """Fetch one page of users starting from offset"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator to lazily paginate through users"""
    offset = 0
    while True:  # only ONE loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
