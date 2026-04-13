from flask import Blueprint

seller_bp = Blueprint("seller", __name__)

from . import routes, api  # noqa: F401, E402