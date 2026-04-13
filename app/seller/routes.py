from flask import render_template
from app.models import Seller, Item
from app.seller import seller_bp


@seller_bp.route("/seller/<int:seller_id>")
def seller_home(seller_id):
    """Seller homepage: view all items, edit business name, toggle shop"""
    seller = Seller.query.get_or_404(seller_id)
    items = Item.query.filter_by(seller_id=seller_id).all()
    return render_template("seller/home.html", seller=seller, items=items)


@seller_bp.route("/seller/<int:seller_id>/items/<int:item_id>")
def seller_item(seller_id, item_id):
    """Seller item detail/edit page"""
    seller = Seller.query.get_or_404(seller_id)
    item = Item.query.filter_by(id=item_id, seller_id=seller_id).first_or_404()
    return render_template("seller/item.html", seller=seller, item=item)