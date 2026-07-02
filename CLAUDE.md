# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the development server
python app.py

# Run tests (pytest)
pytest

# Run a specific test file or test case
pytest tests/test_<filename>.py::<test_function_name>
```

The app runs on `http://localhost:5001` with `debug=True` enabled.


## Architecture

### Overview
This is a Flask-based expense tracker web application with the following high-level structure:

- **Backend**: Flask (Python) with SQLite for data persistence.
- **Frontend**: Jinja2 templates for server-side rendering, with static assets (JavaScript/CSS) for interactivity.
- **Database**: SQLite, initialized and seeded on startup via `database/db.py`.


### Key Components

#### 1. **Flask Application (`app.py`)**
- Sets up the Flask app and initializes the database on startup.
- Defines routes for:
  - Landing page (`/`), registration (`/register`), login (`/login`), and static pages (`/terms`, `/privacy`).
  - Placeholder routes for core functionality (e.g., `/logout`, `/profile`, `/expenses/add`). These are stubs awaiting implementation.

#### 2. **Database Layer (`database/db.py`)**
- Provides functions for:
  - `get_db()`: Returns a SQLite connection with `row_factory` and foreign keys enabled.
  - `init_db()`: Creates tables for `users` and `expenses` if they don’t exist.
  - `seed_db()`: Inserts sample data for development (e.g., a demo user and expenses).
- Uses `bcrypt` for password hashing.

#### 3. **Templates (`templates/`)**
- Base template (`base.html`) defines the shared layout (e.g., navigation, footer).
- Page-specific templates (e.g., `landing.html`, `register.html`) extend `base.html`.
- Includes a modal for embedded videos (e.g., "See how it works" on the landing page).

#### 4. **Static Assets (`static/`)**
- `static/js/main.js`: Client-side JavaScript for interactivity (e.g., modal handling).


### Database Schema

#### Tables
- **`users`**: Stores user accounts with fields for `id`, `username`, `email`, `password_hash`, and `created_at`.
- **`expenses`**: Stores expense records with fields for `id`, `user_id` (foreign key), `amount`, `category`, `description`, `date`, and `created_at`.

#### Relationships
- `expenses.user_id` references `users.id` with `ON DELETE CASCADE`.


### Development Notes

- The project is designed for educational purposes (e.g., placeholder routes are labeled with "students will implement these").
- Sample data is seeded only if the database is empty.
- Passwords are hashed using `bcrypt` before storage.