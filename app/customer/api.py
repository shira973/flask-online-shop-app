from flask import request, jsonify
from app import db
from app.models import Seller, Item, Order
from app.customer import customer_bp


@customer_bp.route("/api/businesses", methods=["GET"])
def get_businesses():
    """Get all businesses with open/closed status"""
    sellers = Seller.query.all()
    return jsonify({
        "success": True,
        "data": [seller.to_dict() for seller in sellers],
    }), 200


@customer_bp.route("/api/businesses/<int:seller_id>/items", methods=["GET"])
def get_business_items(seller_id):
    """Get all items for a specific business"""
    seller = db.session.get(Seller, seller_id)
    if not seller:
        return jsonify({"success": False, "message": "Business not found"}), 404

    items = Item.query.filter_by(seller_id=seller_id).all()
    return jsonify({
        "success": True,
        "data": {
            "business": seller.to_dict(),
            "items": [item.to_dict() for item in items],
        },
    }), 200


@customer_bp.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Get a single item by ID"""
    item = db.session.get(Item, item_id)
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    return jsonify({"success": True, "data": item.to_dict()}), 200


@customer_bp.route("/api/orders", methods=["POST"])
def create_order():
    """Place an order. Expects: item_id, customer_name, customer_contact, quantity"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No JSON data provided"}), 400

    item_id = data.get("item_id")
    customer_name = data.get("customer_name")
    customer_contact = data.get("customer_contact")

    if not item_id or not customer_name or not customer_contact:
        return jsonify({
            "success": False,
            "message": "item_id, customer_name, and customer_contact are required",
        }), 400

    item = db.session.get(Item, item_id)
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    # Check if shop is open
    seller = db.session.get(Seller, item.seller_id)
    if seller and not seller.is_open:
        return jsonify({"success": False, "message": "This shop is currently closed"}), 400

    try:
        quantity = int(data.get("quantity", 1))
        if quantity < 1:
            return jsonify({"success": False, "message": "Quantity must be at least 1"}), 400

        order = Order(
            item_id=item_id,
            seller_id=item.seller_id,
            customer_name=customer_name,
            customer_contact=customer_contact,
            quantity=quantity,
        )

        db.session.add(order)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": order.to_dict(),
            "message": "Order placed successfully",
        }), 201
    except ValueError:
        return jsonify({"success": False, "message": "Invalid quantity"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500