# Task Spec: Digital Shopping Platform

## Files to Create/Modify
- `requirements.txt` — Python dependencies
- `run.py` — Application entry point
- `seed.py` — Demo data seeder
- `app/__init__.py` — App factory
- `app/config.py` — Configuration
- `app/models.py` — Database models
- `app/seller/__init__.py` — Seller blueprint
- `app/seller/routes.py` — Seller page routes
- `app/seller/api.py` — Seller API endpoints
- `app/customer/__init__.py` — Customer blueprint
- `app/customer/routes.py` — Customer page routes
- `app/customer/api.py` — Customer API endpoints
- `app/templates/base.html` — Base layout
- `app/templates/seller/home.html` — Seller homepage
- `app/templates/seller/item.html` — Seller item detail
- `app/templates/customer/businesses.html` — All businesses
- `app/templates/customer/business_items.html` — Business items
- `app/templates/customer/item.html` — Customer item detail
- `tests/conftest.py` — Test fixtures
- `tests/test_seller_api.py` — Seller API tests
- `tests/test_customer_api.py` — Customer API tests
- `tests/test_models.py` — Model tests

## Acceptance Criteria

### Seller API
- [ ] POST /api/seller/items creates an item with name, description, price, contact_details
- [ ] PATCH /api/seller/items/<id> updates item name, description, or price
- [ ] GET /api/seller/items?seller_id=X returns all items for a seller
- [ ] GET /api/seller/items/<id> returns a single item
- [ ] POST /api/seller/toggle-shop toggles shop open/close status
- [ ] PATCH /api/seller/business updates business name

### Customer API
- [ ] GET /api/businesses returns all businesses with open/closed status
- [ ] GET /api/businesses/<id>/items returns all items for a business
- [ ] GET /api/items/<id> returns a single item
- [ ] POST /api/orders places an order with customer_name, customer_contact, quantity

### Seller Pages
- [ ] /seller/<id> shows all items with edit options for business name
- [ ] /seller/<id> shows toggle for open/close shop
- [ ] /seller/<id>/items/<item_id> shows item with edit options for name, description, price
- [ ] Seller can add new items from homepage

### Customer Pages
- [ ] / shows all businesses with open/closed badges
- [ ] /business/<id> shows a business's item list
- [ ] /item/<id> shows individual item detail with order form

### Testing
- [ ] Unit tests for all API endpoints (happy path + error cases)
- [ ] Unit tests for model creation and relationships
- [ ] Integration tests for page rendering

## Edge Cases
- Creating item with missing required fields → 400 error
- Updating non-existent item → 404 error
- Ordering from closed shop → appropriate response
- Invalid quantity → validation error