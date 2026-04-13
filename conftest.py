import pytest
from app import create_app, db as _db
from app.models import Seller, Item


@pytest.fixture(scope="function")
def app():
    """Create application for testing with fresh database."""
    from app.config import TestingConfig
    app = create_app(TestingConfig)

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def sample_seller(app):
    """Create a sample seller."""
    with app.app_context():
        seller = Seller(business_name="Test Shop", contact_details="test@shop.com", is_open=True)
        _db.session.add(seller)
        _db.session.commit()
        # Refresh to get the id
        _db.session.refresh(seller)
        seller_id = seller.id
    return seller_id


@pytest.fixture(scope="function")
def sample_item(app, sample_seller):
    """Create a sample item."""
    with app.app_context():
        item = Item(
            seller_id=sample_seller,
            name="Test Item",
            description="A test item",
            price=9.99,
        )
        _db.session.add(item)
        _db.session.commit()
        _db.session.refresh(item)
        item_id = item.id
    return item_id