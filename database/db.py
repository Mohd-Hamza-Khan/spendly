import sqlite3


def get_db():
    """Return a database connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect("expense_tracker.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all database tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """Insert sample data for development."""
    import bcrypt
    from datetime import date

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    password_hash = bcrypt.hashpw("demo123".encode("utf-8"), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        ("demo", "demo@example.com", password_hash)
    )
    user_id = cursor.lastrowid

    expenses = [
        (user_id, 15.50, "Food", "Lunch at cafe", date(2025, 5, 20)),
        (user_id, 45.00, "Transport", "Uber ride", date(2025, 5, 19)),
        (user_id, 12.99, "Entertainment", "Movie ticket", date(2025, 5, 18)),
        (user_id, 85.00, "Utilities", "Electricity bill", date(2025, 5, 15)),
        (user_id, 28.75, "Food", "Grocery shopping", date(2025, 5, 14)),
    ]

    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
        expenses
    )

    conn.commit()
    conn.close()