import os
import pytest
from src.app import create_app
from src.config import TestConfig
from src.utils.extensions import db

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()