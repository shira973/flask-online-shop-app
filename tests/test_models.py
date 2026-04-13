"""Tests for database models."""
from app import db as _db
from app.models import Seller, Item, Order


class TestSellerModel:
    def test_create_seller(self, app):
        with app.app_context():
            seller = Seller(business_name="My Shop", contact_details="shop@test.com")
            _db.session.add(seller)
            _db.session.commit()
            assert seller.id is not None
            assert seller.is_open is True  # default
            assert seller.created_at is not None

    def test_seller_to_dict(self, app):
        with app.app_context():
            seller = Seller(business_name="Dict Shop", contact_details="dict@test.com")
            _db.session.add(seller)
            _db.session.commit()
            d = seller.to_dict()
            assert d["business_name"] == "Dict Shop"
            assert d["is_open"] is True
            assert "id" in d

    def test_seller_item_relationship(self, app):
        with app.app_context():
            seller = Seller(business_name="Rel Shop")
            _db.session.add(seller)
            _db.session.flush()
            item = Item(seller_id=seller.id, name="Test", price=10.00)
            _db.session.add(item)
            _db.session.commit()
            assert len(seller.items) == 1
            assert seller.items[0].name == "Test"


class TestItemModel:
    def test_create_item(self, app, sample_seller):
        with app.app_context():
            item = Item(seller_id=sample_seller, name="Test Item", description="Desc", price=15.99)
            _db.session.add(item)
            _db.session.commit()
            assert item.id is not None
            assert float(item.price) == 15.99

    def test_item_to_dict(self, app, sample_seller):
        with app.app_context():
            item = Item(seller_id=sample_seller, name="Dict Item", price=5.00)
            _db.session.add(item)
            _db.session.commit()
            d = item.to_dict()
            assert d["name"] == "Dict Item"
            assert d["price"] == 5.00
            assert d["seller_id"] == sample_seller


class TestOrderModel:
    def test_create_order(self, app, sample_seller, sample_item):
        with app.app_context():
            order = Order(
                item_id=sample_item,
                seller_id=sample_seller,
                customer_name="John",
                customer_contact="john@test.com",
                quantity=3,
            )
            _db.session.add(order)
            _db.session.commit()
            assert order.id is not None
            assert order.quantity == 3

    def test_order_to_dict(self, app, sample_seller, sample_item):
        with app.app_context():
            order = Order(
                item_id=sample_item,
                seller_id=sample_seller,
                customer_name="Jane",
                customer_contact="jane@test.com",
                quantity=1,
            )
            _db.session.add(order)
            _db.session.commit()
            d = order.to_dict()
            assert d["customer_name"] == "Jane"
            assert d["quantity"] == 1
            assert d["item_id"] == sample_item