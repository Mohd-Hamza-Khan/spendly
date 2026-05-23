# Expense Tracker - Technical Specification

## 1. Project Overview

A Flask-based expense tracking web application with user authentication and expense management capabilities. Uses SQLite as the database.

---

## 2. Database Schema

### 2.1 Users Table

| Column | Type | Constraints | Description |
|--------|------|--------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique user identifier |
| `username` | TEXT | NOT NULL UNIQUE | User's login name |
| `email` | TEXT | NOT NULL UNIQUE | User's email address |
| `password_hash` | TEXT | NOT NULL | Bcrypt hashed password |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation time |

### 2.2 Expenses Table

| Column | Type | Constraints | Description |
|--------|------|--------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique expense identifier |
| `user_id` | INTEGER | NOT NULL, FOREIGN KEY → users(id) | Owner of the expense |
| `amount` | REAL | NOT NULL | Expense amount (decimal) |
| `category` | TEXT | NOT NULL | Expense category (e.g., Food, Transport) |
| `description` | TEXT | | Optional expense description |
| `date` | DATE | NOT NULL | Date of the expense |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

---

## 3. Database Functions (database/db.py)

### 3.1 get_db()

**Purpose**: Returns a SQLite database connection.

**Requirements**:
- Open connection to `expense_tracker.db`
- Set `row_factory` to `sqlite3.Row` for dict-like access
- Enable foreign keys with `PRAGMA foreign_keys = ON`
- Return the connection object

**Location**: `database/db.py`

```python
def get_db():
    """Return a database connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect("expense_tracker.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
```

### 3.2 init_db()

**Purpose**: Initialize database schema by creating all tables.

**Requirements**:
- Create `users` table with schema defined in Section 2.1
- Create `expenses` table with schema defined in Section 2.2
- Use `CREATE TABLE IF NOT EXISTS` to make it idempotent
- Call this once at application startup

**Location**: `database/db.py`

```python
def init_db():
    """Create all database tables if they don't exist."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create expenses table
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
```

### 3.3 seed_db()

**Purpose**: Insert sample data for development/testing.

**Requirements**:
- Create at least one demo user (username: `demo`, password: `demo123`)
- Create 3-5 sample expenses linked to the demo user
- Include varied categories: Food, Transport, Entertainment, Utilities
- Only insert if tables are empty (check before seeding)

**Location**: `database/db.py`

```python
def seed_db():
    """Insert sample data for development."""
    import bcrypt
    from datetime import date
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Create demo user (password: demo123)
    password_hash = bcrypt.hashpw("demo123".encode("utf-8"), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        ("demo", "demo@example.com", password_hash)
    )
    user_id = cursor.lastrowid
    
    # Sample expenses
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
```

---

## 4. Changes to app.py

### 4.1 Add Imports

Add at the top of `app.py`:

```python
from database.db import get_db, init_db, seed_db
```

### 4.2 Initialize Database on Startup

Add before route definitions:

```python
# Initialize database on startup
with app.app_context():
    init_db()
    seed_db()
```

### 4.3 Full Updated app.py Structure

```python
from flask import Flask, render_template
from database.db import get_db, init_db, seed_db

app = Flask(__name__)

# Initialize database on startup
with app.app_context():
    init_db()
    seed_db()

# ... all routes remain unchanged ...

if __name__ == "__main__":
    app.run(debug=True, port=5001)
```

---

## 5. Files to Modify

| File | Changes |
|------|---------|
| `database/db.py` | Implement `get_db()`, `init_db()`, `seed_db()` functions |
| `app.py` | Add database imports and startup initialization |

---

## 6. Dependencies

No new pip packages required. Uses:
- `sqlite3` (built-in Python)
- `bcrypt` (already available in project environment for password hashing)

---

## 7. Implementation Order

1. **database/db.py**: Implement all three functions
2. **app.py**: Add imports and initialization call
3. **Test**: Run `python app.py` and verify:
   - Database file `expense_tracker.db` is created
   - Tables `users` and `expenses` exist
   - Sample data is present
   - Routes work correctly

---

## 8. Future Considerations (Not in Scope)

- User authentication routes (/register, /login POST handlers)
- Session management
- Expense CRUD operations
- Input validation
- Error handling
- Password reset functionality