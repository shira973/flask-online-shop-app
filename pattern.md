# Digital Shopping Platform — Patterns

## Coding Standards
- Python: PEP 8, 4-space indent
- HTML: 2-space indent, Bootstrap 5 classes
- API responses: JSON with consistent shape `{ "success": bool, "data": ..., "message": ... }`
- Errors: return appropriate HTTP status codes (400, 404, 500)

## Naming
- Models: PascalCase (Seller, Item, Order)
- Routes/API: snake_case (toggle_shop, business_items)
- Templates: snake_case.html
- CSS classes: Bootstrap utility classes, custom `ds-` prefix if needed

## Error Handling
- API: try/except with rollback on DB errors, return JSON error
- Pages: 404 template for missing resources
- Input validation on all POST/PATCH endpoints

## Test Conventions
- pytest with Flask test client
- Test file per module: test_seller_api.py, test_customer_api.py
- Each API endpoint gets at least one test (happy path + error case)
- Fixtures in conftest.py provide clean app + client