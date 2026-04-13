# Digital Shopping Platform — Schema

## Database Tables

### sellers
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | INT | PK, AUTO_INCREMENT | |
| business_name | VARCHAR(255) | NOT NULL | Shop display name |
| contact_details | VARCHAR(255) | | Seller contact info |
| is_open | BOOLEAN | DEFAULT TRUE | Shop open/close status |
| created_at | DATETIME | DEFAULT NOW | |

### items
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | INT | PK, AUTO_INCREMENT | |
| seller_id | INT | FK → sellers.id, NOT NULL | Owner |
| name | VARCHAR(255) | NOT NULL | |
| description | TEXT | | |
| price | DECIMAL(10,2) | NOT NULL | |
| created_at | DATETIME | DEFAULT NOW | |

### orders
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | INT | PK, AUTO_INCREMENT | |
| item_id | INT | FK → items.id, NOT NULL | |
| seller_id | INT | FK → sellers.id, NOT NULL | |
| customer_name | VARCHAR(255) | NOT NULL | |
| customer_contact | VARCHAR(255) | NOT NULL | |
| quantity | INT | NOT NULL, DEFAULT 1 | |
| created_at | DATETIME | DEFAULT NOW | |

## API Endpoints

### Seller API
| Method | Endpoint | Body / Params | Returns |
|--------|----------|---------------|---------|
| POST | /api/seller/items | {seller_id, name, description, price, contact_details} | Created item |
| PATCH | /api/seller/items/<id> | {name?, description?, price?} | Updated item |
| GET | /api/seller/items?seller_id=X | — | List of items |
| GET | /api/seller/items/<id> | — | Single item |
| POST | /api/seller/toggle-shop | {seller_id} | Updated seller status |

### Customer API
| Method | Endpoint | Body / Params | Returns |
|--------|----------|---------------|---------|
| GET | /api/businesses | — | All sellers |
| GET | /api/businesses/<id>/items | — | Items for a seller |
| GET | /api/items/<id> | — | Single item |
| POST | /api/orders | {item_id, customer_name, customer_contact, quantity} | Created order |