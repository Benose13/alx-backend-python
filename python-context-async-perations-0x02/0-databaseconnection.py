import sqlite3


class DatabaseConnection:
    """Custom context manager for handling DB connections"""

    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        # Open database connection
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Rollback if there was an error, else commit
        if exc_type:
            self.conn.rollback()
            print(f"[ERROR] Transaction rolled back: {exc_val}")
        else:
            self.conn.commit()
        # Always close connection
        self.conn.close()
        return False  # Propagate exception if any


# ✅ Using the context manager to fetch users
with DatabaseConnection("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Users in database:")
    for row in results:
        print(row)
