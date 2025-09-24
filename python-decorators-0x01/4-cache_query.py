import time
import sqlite3
import functools


query_cache = {}


def with_db_connection(func):
    """Decorator to automatically open and close DB connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


def cache_query(func):
    """Decorator to cache query results based on SQL query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get SQL query string (must be passed as kwarg or arg)
        query = kwargs.get("query")
        if query is None and len(args) > 1:
            query = args[1]  # conn is args[0], query should be args[1]

        # Return cached result if available
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            return query_cache[query]

        # Otherwise, execute the function and cache result
        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE MISS] Caching result for: {query}")
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# ✅ First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# ✅ Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users)
print(users_again)
