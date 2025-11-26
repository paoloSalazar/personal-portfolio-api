# Personal Portfolio API

This project is a Flask REST API designed for managing user information in a personal portfolio application. It allows users to create, read, update, and delete their personal information, projects, and skills.

## Project Structure

- **src/**: Contains the main application code.
  - **app.py**: Entry point of the application.
  - **config.py**: Configuration settings for the Flask application.
  - **models/**: Contains data models.
    - **user.py**: Defines the User model.
  - **schemas/**: Contains schemas for data serialization.
    - **user_schema.py**: Defines the UserSchema for the User model.
  - **resources/**: Contains resource classes for API endpoints.
    - **user_resource.py**: Defines user-related API endpoints.
  - **routes/**: Contains route definitions.
    - **api.py**: Sets up API routes.
  - **services/**: Contains business logic.
    - **user_service.py**: User management logic.
  - **utils/**: Contains utility functions and extensions.
    - **extensions.py**: Initializes and configures extensions.

- **tests/**: Contains unit tests for the application.
  - **test_user.py**: Unit tests for user functionalities.
  - **conftest.py**: Test fixtures.

- **requirements.txt**: Lists project dependencies.
- **.env**: Contains environment variables for configuration.
- **Dockerfile**: Instructions for building a Docker image.
- **pyproject.toml**: Manages project dependencies and configurations.
- **README.md**: Documentation for the project.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd personal-portfolio-api
   ```

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables in the `.env` file.

## Usage

To run the application, execute:
```
python src/app.py
```

The API will be available at `http://localhost:5000`.

## Migrations
To run migrations execute the next commands
```bash
# then use:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Testing

To run the tests, use:
```
pytest tests/
```

## License

This project is licensed under the MIT License.