# Digital Shopping Platform — Architecture

## Directory Structure
```
/workspace/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Config classes
│   ├── models.py            # SQLAlchemy models
│   ├── seller/
│   │   ├── __init__.py
│   │   ├── routes.py        # Seller page routes
│   │   └── api.py           # Seller API routes
│   ├── customer/
│   │   ├── __init__.py
│   │   ├── routes.py        # Customer page routes
│   │   └── api.py           # Customer API routes
│   └── templates/
│       ├── base.html
│       ├── seller/
│       │   ├── home.html
│       │   └── item.html
│       └── customer/
│           ├── businesses.html
│           ├── business_items.html
│           └── item.html
├── tests/
│   ├── conftest.py
│   ├── test_seller_api.py
│   ├── test_customer_api.py
│   └── test_models.py
├── seed.py                  # Demo data seeder
├── run.py                   # Entry point
├── requirements.txt
└── .drytis/
```

## Data Flow
1. Flask app factory creates app with SQLAlchemy + blueprints
2. Seller pages: server-rendered with Alpine.js for AJAX calls to API
3. Customer pages: server-rendered, order form posts to API
4. All data mutations go through `/api/` endpoints (JSON)
5. Page routes render templates with data from models

## Routing
- `/seller/<id>` → Seller homepage
- `/seller/<id>/items/<item_id>` → Seller item detail/edit
- `/` → Customer businesses list
- `/business/<id>` → Customer business items
- `/item/<id>` → Customer item detail