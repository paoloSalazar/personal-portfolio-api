from flask import Flask
from config import Config
from routes.api import api_bp
from utils.extensions import db
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

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