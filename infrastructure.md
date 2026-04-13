# Digital Shopping Platform — Infrastructure

## Environment Variables
- `DATABASE_URL`: MySQL connection string
- `FLASK_ENV`: development / production
- `SECRET_KEY`: Flask session secret

## Proxy Routes
- Caddy reverse proxy: `/` → `localhost:5000`

## Background Services
- Flask dev server: `flask run --host=0.0.0.0 --port=5000`

## Database
- MySQL 8.x on localhost:3306
- DB: u1056p1580_digital_shop
- Auto-create tables via SQLAlchemy on startup

## Ports
- 5000: Flask application