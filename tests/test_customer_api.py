"""Tests for Customer API endpoints."""
import pytest


class TestGetBusinesses:
    def test_get_all_businesses(self, client, sample_seller):
        res = client.get("/api/businesses")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["data"]) >= 1
        # Check the business has open/closed status
        biz = data["data"][0]
        assert "is_open" in biz
        assert "business_name" in biz

    def test_get_businesses_empty(self, client, app):
        res = client.get("/api/businesses")
        assert res.status_code == 200
        assert len(res.get_json()["data"]) == 0


class TestGetBusinessItems:
    def test_get_business_items(self, client, sample_seller, sample_item):
        res = client.get(f"/api/businesses/{sample_seller}/items")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert "business" in data["data"]
        assert "items" in data["data"]
        assert len(data["data"]["items"]) >= 1

    def test_get_business_items_invalid(self, client):
        res = client.get("/api/businesses/9999/items")
        assert res.status_code == 404


class TestGetItem:
    def test_get_single_item(self, client, sample_item):
        res = client.get(f"/api/items/{sample_item}")
        assert res.status_code == 200
        data = res.get_json()
        assert data["data"]["name"] == "Test Item"

    def test_get_nonexistent_item(self, client):
        res = client.get("/api/items/9999")
        assert res.status_code == 404


class TestCreateOrder:
    def test_create_order_success(self, client, sample_item):
        res = client.post("/api/orders", json={
            "item_id": sample_item,
            "customer_name": "John Doe",
            "customer_contact": "john@example.com",
            "quantity": 2,
        })
        assert res.status_code == 201
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["customer_name"] == "John Doe"
        assert data["data"]["quantity"] == 2

    def test_create_order_default_quantity(self, client, sample_item):
        res = client.post("/api/orders", json={
            "item_id": sample_item,
            "customer_name": "Jane",
            "customer_contact": "jane@test.com",
        })
        assert res.status_code == 201
        assert res.get_json()["data"]["quantity"] == 1

    def test_create_order_missing_fields(self, client, sample_item):
        res = client.post("/api/orders", json={
            "item_id": sample_item,
        })
        assert res.status_code == 400

    def test_create_order_invalid_item(self, client):
        res = client.post("/api/orders", json={
            "item_id": 9999,
            "customer_name": "Test",
            "customer_contact": "test@test.com",
        })
        assert res.status_code == 404

    def test_create_order_closed_shop(self, client, app, sample_seller, sample_item):
        # Close the shop first
        from app.models import Seller
        seller = Seller.query.get(sample_seller)
        seller.is_open = False
        from app import db
        db.session.commit()

        res = client.post("/api/orders", json={
            "item_id": sample_item,
            "customer_name": "Test",
            "customer_contact": "test@test.com",
            "quantity": 1,
        })
        assert res.status_code == 400
        assert "closed" in res.get_json()["message"].lower()

    def test_create_order_invalid_quantity(self, client, sample_item):
        res = client.post("/api/orders", json={
            "item_id": sample_item,
            "customer_name": "Test",
            "customer_contact": "test@test.com",
            "quantity": 0,
        })
        assert res.status_code == 400

    def test_create_order_no_data(self, client):
        res = client.post("/api/orders", content_type="application/json")
        assert res.status_code == 400