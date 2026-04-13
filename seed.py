"""Seed the database with demo data."""
from app import create_app, db
from app.models import Seller, Item

app = create_app()

with app.app_context():
    db.create_all()

    # Create demo sellers
    sellers_data = [
        {"business_name": "Fresh Bakery", "contact_details": "fresh@bakery.com", "is_open": True},
        {"business_name": "Tech Gadgets", "contact_details": "555-0123", "is_open": True},
        {"business_name": "Green Garden", "contact_details": "garden@green.com", "is_open": False},
    ]

    sellers = []
    for sd in sellers_data:
        seller = Seller(**sd)
        db.session.add(seller)
        sellers.append(seller)

    db.session.flush()

    # Create demo items
    items_data = [
        {"seller_id": sellers[0].id, "name": "Sourdough Bread", "description": "Freshly baked sourdough loaf made with organic flour", "price": 5.99},
        {"seller_id": sellers[0].id, "name": "Chocolate Cake", "description": "Rich chocolate cake with ganache frosting", "price": 24.99},
        {"seller_id": sellers[0].id, "name": "Croissants (4 pack)", "description": "Buttery, flaky French croissants", "price": 8.50},
        {"seller_id": sellers[1].id, "name": "Wireless Earbuds", "description": "Bluetooth 5.3 noise-cancelling earbuds with 24h battery", "price": 49.99},
        {"seller_id": sellers[1].id, "name": "USB-C Hub", "description": "7-in-1 USB-C hub with HDMI, USB 3.0, SD card reader", "price": 34.99},
        {"seller_id": sellers[2].id, "name": "Succulent Pack", "description": "Pack of 4 assorted succulents", "price": 15.00},
        {"seller_id": sellers[2].id, "name": "Herb Garden Kit", "description": "Indoor herb growing kit with basil, mint, and cilantro seeds", "price": 22.50},
    ]

    for item_data in items_data:
        item = Item(**item_data)
        db.session.add(item)

    db.session.commit()

    print("✅ Seed data created successfully!")
    print(f"   {len(sellers)} sellers, {len(items_data)} items")
    for s in sellers:
        print(f"   Seller {s.id}: {s.business_name} ({'Open' if s.is_open else 'Closed'}) — /seller/{s.id}")