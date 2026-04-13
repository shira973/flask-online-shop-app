# Digital Shopping Platform — Spec

## Overview
A Flask-based digital shopping platform with separate seller and customer portals. Sellers manage their shop, items, and open/close status. Customers browse businesses, view items, and place orders.

## Tech Stack
- **Backend**: Flask 3.x (Python 3)
- **Frontend**: Jinja2 templates, Bootstrap 5, Alpine.js for reactivity
- **Database**: MySQL via Flask-SQLAlchemy
- **Testing**: pytest + Flask test client

## Key Decisions
- Single Flask app with blueprints for seller and customer routes
- REST JSON API under `/api/` for all data operations
- Server-side rendered pages with Alpine.js for interactive bits (modals, inline edits)
- No authentication required (seller identified by URL `/seller/<id>`)
- Seed data script for demo purposes