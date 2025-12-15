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

### authentications not working
Getting Authentication failed when using a protected endpoint
```json
POST {{api}}/contacttypes
Content-Type: application/json
Authorization: Bearer {{user_token}}

{
    "name": "emailnew",
    "description": "Contact via email"
}
```
response
```

FIX
auth_resource.py
```python
# convert identity to str
access_token = create_access_token(identity=str(user.id))
refresh_token = create_refresh_token(identity=str(user.id))
```

### duplicated migration revisions and heads
```bash
$ flask db upgrade
INFO [alembic.runtime.migration] Context impl MySQLImpl.
INFO [alembic.runtime.migration] Will assume non-transactional DDL.
ERROR [flask_migrate] Error: Multiple head revisions are present for given argument 'head'; please specify a specific target revision, '<branchname>@head' to narrow to a specific head, or 'heads' for all heads
```
FIX

```bash
flask db heads  
466f168ada4d (head)
added_user_skill_entity (head)
```

```bash
$ flask db upgrade
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 4c28f9c63b2a -> added_user_skill_entity, added user_skill entity
INFO  [alembic.runtime.migration] Running upgrade 4c28f9c63b2a -> 466f168ada4d, added user_skill entity for many-to-many relationship
INFO  [alembic.runtime.migration] Running upgrade 466f168ada4d, added_user_skill_entity -> c0195dad3c62, Merge heads
```