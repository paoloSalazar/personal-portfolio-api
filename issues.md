# List of Issues in this project

### Unable to run unit tests
Unable to run unit testing feature due to import errors
both tests and app being affected due to different import sentences.

**FIX** Add try catch blocks to solve import errors
```python
## from app.py
try:
    from config import Config
    from routes.api import api_bp
    from utils.extensions import db
except ImportError:
    from .config import Config
    from .routes.api import api_bp
    from .utils.extensions import db
```

### Development database being removed when tests executed
Database tables being removed when unit tests are executed.

```python
## conftest.py
import os
import pytest
from src.app import create_app
from src.config import TestConfig
from src.utils.extensions import db

@pytest.fixture
def app():
    app = create_app(TestConfig)
    # database being created and removed
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
```

