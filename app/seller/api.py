from flask import request, jsonify
from app import db
from app.models import Seller, Item
from app.seller import seller_bp

@seller_bp.route("/api/seller", methods=["POST"])
def create_seller():
    """Create a new seller. Expects: business_name, contact_details, is_open"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No JSON data provided"}), 400

    business_name = data.get("business_name")
    if not business_name:
        return jsonify({"success": False, "message": "business_name is required"}), 400

    try:
        seller = Seller(
            business_name=business_name,
            contact_details=data.get("contact_details"),
            is_open=data.get("is_open", True),
        )
        db.session.add(seller)
        db.session.commit()

        return jsonify({"success": True, "data": seller.to_dict(), "message": "Seller created"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@seller_bp.route("/api/seller/items", methods=["POST"])
def create_item():
    """Create a new item. Expects: seller_id, name, description, price, contact_details"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "No JSON data provided"}), 400

    seller_id = data.get("seller_id")
    name = data.get("name")
    price = data.get("price")

    if not seller_id or not name or price is None:
        return jsonify({"success": False, "message": "seller_id, name, and price are required"}), 400

    seller = db.session.get(Seller, seller_id)
    if not seller:
        return jsonify({"success": False, "message": "Seller not found"}), 404

    try:
        item = Item(
            seller_id=seller_id,
            name=name,
            description=data.get("description", ""),
            price=price,
        )

        # Update seller contact details if provided
        if data.get("contact_details"):
            seller.contact_details = data["contact_details"]

        db.session.add(item)
        db.session.commit()

        return jsonify({"success": True, "data": item.to_dict(), "message": "Item created"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


@seller_bp.route("/api/seller/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    """Update an item. Accepts: name, description, price"""
    item = db.session.get(Item, item_id)
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "No JSON data provided"}), 400

    try:
        if "name" in data:
            item.name = data["name"]
        if "description" in data:
            item.description = data["description"]
        if "price" in data:
            item.price = data["price"]

        db.session.commit()

        return jsonify({"success": True, "data": item.to_dict(), "message": "Item updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


@seller_bp.route("/api/seller/items", methods=["GET"])
def get_items():
    """Get all items for a seller. Query param: seller_id"""
    seller_id = request.args.get("seller_id")
    if not seller_id:
        return jsonify({"success": False, "message": "seller_id query parameter is required"}), 400

    seller = db.session.get(Seller, int(seller_id))
    if not seller:
        return jsonify({"success": False, "message": "Seller not found"}), 404

    items = Item.query.filter_by(seller_id=seller_id).all()
    return jsonify({"success": True, "data": [item.to_dict() for item in items]}), 200


@seller_bp.route("/api/seller/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Get a single item by ID"""
    item = db.session.get(Item, item_id)
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    return jsonify({"success": True, "data": item.to_dict()}), 200


@seller_bp.route("/api/seller/toggle-shop", methods=["POST"])
def toggle_shop():
    """Toggle shop open/close status. Expects: seller_id"""
    data = request.get_json(silent=True)
    if not data or not data.get("seller_id"):
        return jsonify({"success": False, "message": "seller_id is required"}), 400

    seller = db.session.get(Seller, data["seller_id"])
    if not seller:
        return jsonify({"success": False, "message": "Seller not found"}), 404

    try:
        seller.is_open = not seller.is_open
        db.session.commit()

        status = "open" if seller.is_open else "closed"
        return jsonify({
            "success": True,
            "data": seller.to_dict(),
            "message": f"Shop is now {status}",
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


@seller_bp.route("/api/seller/business", methods=["PATCH"])
def update_business():
    """Update business name. Expects: seller_id, business_name"""
    data = request.get_json(silent=True)
    if not data or not data.get("seller_id"):
        return jsonify({"success": False, "message": "seller_id is required"}), 400

    seller = db.session.get(Seller, data["seller_id"])
    if not seller:
        return jsonify({"success": False, "message": "Seller not found"}), 404

    try:
        if data.get("business_name"):
            seller.business_name = data["business_name"]
        if data.get("contact_details"):
            seller.contact_details = data["contact_details"]

        db.session.commit()

        return jsonify({
            "success": True,
            "data": seller.to_dict(),
            "message": "Business updated",
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500