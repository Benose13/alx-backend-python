import time
import sqlite3
import functools


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


def retry_on_failure(retries=3, delay=2):
    """Decorator to retry DB operations if transient errors occur"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    # SQLite transient error (like database is locked, etc.)
                    last_exception = e
                    print(f"[Retry {attempt}/{retries}] Transient error: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                except Exception as e:
                    # For any other unexpected errors → do not retry
                    raise
            # If all retries failed, re-raise last exception
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# ✅ Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
