from flask import Flask
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()


from flask_migrate import Migrate

try:
    from config import Config
    from routes.api import api_bp
    from utils.extensions import db
except ImportError:
    from .config import Config
    from .routes.api import api_bp
    from .utils.extensions import db



def create_app(config_class=None):
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        try:
            from .config import Config
        except ImportError:
            from config import Config
        app.config.from_object(Config)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Create database tables (you can remove this when using migrations)
    # with app.app_context():
    #     db.create_all()

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)