# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Expense tracker web application built with Flask. Currently a scaffold with landing pages and placeholder routes — database and core functionality are yet to be implemented.

## Commands

```bash
# Run the development server
python app.py

# Run tests (pytest)
pytest
```

The app runs on `http://localhost:5001` with `debug=True` enabled.

## Architecture

- **Framework**: Flask with Jinja2 templates
- **Database**: SQLite — `database/db.py` contains stub functions (`get_db`, `init_db`, `seed_db`) to be implemented
- **Static**: JavaScript in `static/js/main.js`
- **Templates**: `templates/` — base layout in `base.html`, pages extend it

### Routes

| Route | Purpose |
|-------|---------|
| `/` | Landing page with dashboard preview |
| `/register` | User registration |
| `/login` | User login |
| `/terms` | Terms of service |
| `/privacy` | Privacy policy |
| `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` | Placeholders — not yet implemented |

## Key Files

- `app.py` — Flask app setup and all routes
- `database/db.py` — Database connection and initialization (student implementation)
- `templates/landing.html` — Main landing page with embedded video modal
- `static/js/main.js` — Client-side JavaScript

## Notes

The project appears to be educational (see comments in `database/db.py` referencing "students"). The database layer and several core features are placeholder code awaiting implementation.