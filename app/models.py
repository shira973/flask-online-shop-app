from datetime import datetime, timezone
from app import db


class Seller(db.Model):
    __tablename__ = "sellers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_name = db.Column(db.String(255), nullable=False, default="My Shop")
    contact_details = db.Column(db.String(255), nullable=True)
    is_open = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    items = db.relationship("Item", backref="seller", lazy=True)
    orders = db.relationship("Order", backref="seller", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "business_name": self.business_name,
            "contact_details": self.contact_details,
            "is_open": self.is_open,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "item_count": len(self.items),
        }


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    orders = db.relationship("Order", backref="item", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey("sellers.id"), nullable=False)
    customer_name = db.Column(db.String(255), nullable=False)
    customer_contact = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "item_id": self.item_id,
            "seller_id": self.seller_id,
            "customer_name": self.customer_name,
            "customer_contact": self.customer_contact,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }