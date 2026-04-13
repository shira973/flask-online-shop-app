from flask import render_template
from app.models import Seller, Item
from app.customer import customer_bp


@customer_bp.route("/")
def businesses():
    """Customer landing page: list all businesses"""
    sellers = Seller.query.all()
    return render_template("customer/businesses.html", sellers=sellers)


@customer_bp.route("/business/<int:seller_id>")
def business_items(seller_id):
    """Customer view: a business's item list"""
    seller = Seller.query.get_or_404(seller_id)
    items = Item.query.filter_by(seller_id=seller_id).all()
    return render_template("customer/business_items.html", seller=seller, items=items)


@customer_bp.route("/item/<int:item_id>")
def item_detail(item_id):
    """Customer view: individual item detail with order form"""
    item = Item.query.get_or_404(item_id)
    seller = Seller.query.get(item.seller_id)
    return render_template("customer/item.html", item=item, seller=seller)