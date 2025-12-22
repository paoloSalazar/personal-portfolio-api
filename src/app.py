from flask import Flask, jsonify, request, g
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import time

# Load environment variables
load_dotenv()


from flask_migrate import Migrate

try:
    from config import Config
    from routes.api import api_bp
    from utils.extensions import db, jwt
    # Import models to ensure they are registered with SQLAlchemy
    from models.user import User
    from models.contact_type import ContactType
    from models.skill import Skill
    from models.user_skill import UserSkill
    from models.user_contact import UserContact
except ImportError:
    from .config import Config
    from .routes.api import api_bp
    from .utils.extensions import db, jwt
    # Import models to ensure they are registered with SQLAlchemy
    from .models.user import User
    from .models.contact_type import ContactType
    from .models.skill import Skill
    from .models.user_skill import UserSkill
    from .models.user_contact import UserContact


logger = logging.getLogger(__name__)



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
    jwt.init_app(app)
    migrate = Migrate(app, db)

    # Initialize CORS for React frontend integration
    CORS(app)

    # Create database tables (you can remove this when using migrations)
    # with app.app_context():
    #     db.create_all()

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    # Request logging middleware
    @app.before_request
    def log_request_info():
        g.start_time = time.time()
        logger.info(f"Request: {request.method} {request.url} from {request.remote_addr}")

    @app.after_request
    def log_response_info(response):
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            logger.info(f"Response: {response.status_code} in {duration:.4f}s")
        return response

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not Found', 'message': 'Resource not found'}), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({'error': 'Unprocessable Entity', 'message': str(error)}), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal Server Error', 'message': 'Something went wrong'}), 500

    # Handle custom exceptions
    try:
        from exceptions.user_exceptions import UserException
        from exceptions.contact_type_exceptions import ContactTypeException

        @app.errorhandler(UserException)
        def handle_user_exception(error):
            return jsonify({'error': error.message}), error.status_code

        @app.errorhandler(ContactTypeException)
        def handle_contact_type_exception(error):
            return jsonify({'error': error.message}), error.status_code
    except ImportError:
        # Handle imports for different module structures
        try:
            from src.exceptions.user_exceptions import UserException
            from src.exceptions.contact_type_exceptions import ContactTypeException

            @app.errorhandler(UserException)
            def handle_user_exception(error):
                return jsonify({'error': error.message}), error.status_code

            @app.errorhandler(ContactTypeException)
            def handle_contact_type_exception(error):
                return jsonify({'error': error.message}), error.status_code
        except ImportError:
            pass  # Exceptions not available, skip custom handlers

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)