import os
import pytest
from app import create_app
from app.models import db as _db

TEST_CONFIG = {
    "TESTING": True,
    "WTF_CSRF_ENABLED": False,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "SECRET_KEY": "test-secret-key",
    "UPLOAD_FOLDER": "/tmp/ashnote_test_uploads",
    "RATELIMIT_ENABLED": False,
}


@pytest.fixture(scope="session")
def app():
    os.makedirs(TEST_CONFIG["UPLOAD_FOLDER"], exist_ok=True)
    test_app = create_app(test_config=TEST_CONFIG)

    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Rol de database terug na elke test voor isolatie."""
    with app.app_context():
        yield
        _db.session.rollback()
