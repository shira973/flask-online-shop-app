"""Tests for Seller API endpoints."""
import json


class TestCreateItem:
    def test_create_item_success(self, client, sample_seller):
        res = client.post("/api/seller/items", json={
            "seller_id": sample_seller,
            "name": "New Item",
            "description": "A brand new item",
            "price": 19.99,
            "contact_details": "seller@test.com",
        })
        assert res.status_code == 201
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["name"] == "New Item"
        assert float(data["data"]["price"]) == 19.99

    def test_create_item_missing_fields(self, client, sample_seller):
        res = client.post("/api/seller/items", json={
            "seller_id": sample_seller,
        })
        assert res.status_code == 400
        data = res.get_json()
        assert data["success"] is False

    def test_create_item_invalid_seller(self, client):
        res = client.post("/api/seller/items", json={
            "seller_id": 9999,
            "name": "Item",
            "price": 10.00,
        })
        assert res.status_code == 404

    def test_create_item_no_data(self, client, sample_seller):
        res = client.post("/api/seller/items", content_type="application/json")
        assert res.status_code == 400


class TestUpdateItem:
    def test_update_item_name(self, client, sample_item):
        res = client.patch(f"/api/seller/items/{sample_item}", json={
            "name": "Updated Item",
        })
        assert res.status_code == 200
        data = res.get_json()
        assert data["data"]["name"] == "Updated Item"

    def test_update_item_price(self, client, sample_item):
        res = client.patch(f"/api/seller/items/{sample_item}", json={
            "price": 29.99,
        })
        assert res.status_code == 200
        assert float(res.get_json()["data"]["price"]) == 29.99

    def test_update_item_description(self, client, sample_item):
        res = client.patch(f"/api/seller/items/{sample_item}", json={
            "description": "Updated description",
        })
        assert res.status_code == 200
        assert res.get_json()["data"]["description"] == "Updated description"

    def test_update_nonexistent_item(self, client):
        res = client.patch("/api/seller/items/9999", json={"name": "X"})
        assert res.status_code == 404

    def test_update_item_no_data(self, client, sample_item):
        res = client.patch(f"/api/seller/items/{sample_item}", content_type="application/json")
        assert res.status_code == 400


class TestGetItems:
    def test_get_all_items(self, client, sample_seller, sample_item):
        res = client.get(f"/api/seller/items?seller_id={sample_seller}")
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert len(data["data"]) >= 1

    def test_get_items_missing_seller_id(self, client):
        res = client.get("/api/seller/items")
        assert res.status_code == 400

    def test_get_items_invalid_seller(self, client):
        res = client.get("/api/seller/items?seller_id=9999")
        assert res.status_code == 404


class TestGetItem:
    def test_get_single_item(self, client, sample_item):
        res = client.get(f"/api/seller/items/{sample_item}")
        assert res.status_code == 200
        data = res.get_json()
        assert data["data"]["name"] == "Test Item"

    def test_get_nonexistent_item(self, client):
        res = client.get("/api/seller/items/9999")
        assert res.status_code == 404


class TestToggleShop:
    def test_toggle_shop_open_to_closed(self, client, sample_seller):
        res = client.post("/api/seller/toggle-shop", json={
            "seller_id": sample_seller,
        })
        assert res.status_code == 200
        data = res.get_json()
        assert data["data"]["is_open"] is False

    def test_toggle_shop_back_to_open(self, client, sample_seller):
        # Toggle twice
        client.post("/api/seller/toggle-shop", json={"seller_id": sample_seller})
        res = client.post("/api/seller/toggle-shop", json={"seller_id": sample_seller})
        data = res.get_json()
        assert data["data"]["is_open"] is True

    def test_toggle_shop_missing_seller(self, client):
        res = client.post("/api/seller/toggle-shop", json={})
        assert res.status_code == 400

    def test_toggle_shop_invalid_seller(self, client):
        res = client.post("/api/seller/toggle-shop", json={"seller_id": 9999})
        assert res.status_code == 404


class TestUpdateBusiness:
    def test_update_business_name(self, client, sample_seller):
        res = client.patch("/api/seller/business", json={
            "seller_id": sample_seller,
            "business_name": "New Shop Name",
        })
        assert res.status_code == 200
        assert res.get_json()["data"]["business_name"] == "New Shop Name"

    def test_update_business_contact(self, client, sample_seller):
        res = client.patch("/api/seller/business", json={
            "seller_id": sample_seller,
            "contact_details": "new@contact.com",
        })
        assert res.status_code == 200
        assert res.get_json()["data"]["contact_details"] == "new@contact.com"

    def test_update_business_missing_seller(self, client):
        res = client.patch("/api/seller/business", json={
            "business_name": "Test",
        })
        assert res.status_code == 400