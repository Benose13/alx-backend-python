import sqlite3


class ExecuteQuery:
    """Custom context manager to execute a query with parameters"""

    def __init__(self, query, params=None, db_name="users.db"):
        self.db_name = db_name
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        # Execute query with parameters
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # Returned to the 'as' variable in with

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
            print(f"[ERROR] Rolling back: {exc_val}")
        else:
            self.conn.commit()
        self.conn.close()
        return False  # Do not suppress exceptions


# ✅ Usage
with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print("Users older than 25:")
    for row in results:
        print(row)
