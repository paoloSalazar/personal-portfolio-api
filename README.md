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

## Debug with VSCode
To use VS Code breakpoints instead of terminal, create a debug configuration file.

Create .vscode/launch.json in your project root:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask App",
            "type": "debugpy",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "src.app:create_app",
                "FLASK_ENV": "development",
                "PYTHONPATH": "${workspaceFolder}"
            },
            "args": ["run", "--debug"],
            "jinja": true,
            "justMyCode": true
        },
        {
            "name": "Pytest",
            "type": "debugpy",
            "request": "launch",
            "module": "pytest",
            "args": ["./tests", "-v", "--tb=short"],
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```
To debug:

1\. Click the line number in [user_service.py]user_service.py ) to set a breakpoint (red dot)
2\. Open Run & Debug in VS Code (Ctrl+Shift+D)
3\. Select "Flask App" or "Pytest" from dropdown
4\. Press F5 to start debugging
5\. When code hits your breakpoint, execution pauses and you can:
* Hover over variables to inspect values
* Use Debug Console to run commands
* Step through code (F10 = step over, F11 = step into)

The debugger will stop at your breakpoint in [create_user()]user_service.py ) function.

## License

This project is licensed under the MIT License.