from flask import Blueprint

customer_bp = Blueprint("customer", __name__)

from . import routes, api  # noqa: F401, E402