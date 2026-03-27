import os
from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig, TestingConfig, ProductionConfig
from .routes.quiz_routes import quiz_routes_v1_bp
from .routes.auth_routes import auth_routes_v1_bp
from .utils.exceptions import JWTError, ServiceError, RepositoryError
from .utils.responses import error_response


def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object(ProductionConfig)
    elif env == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    CORS(
        app,
        supports_credentials=True,
        origins=os.getenv("CORS_ORIGINS", "").split(","),
    )

    app.register_blueprint(auth_routes_v1_bp, url_prefix="/api")
    app.register_blueprint(quiz_routes_v1_bp, url_prefix="/api")

    # Global error handlers
    @app.errorhandler(JWTError)
    def handle_jwt_errors(e):
        return error_response(str(e), 401)

    @app.errorhandler(ServiceError)
    def handle_service_errors(e):
        return error_response(str(e), 400)

    @app.errorhandler(RepositoryError)
    def handle_repository_errors(e):
        if env == "production":
            return error_response("Database error", 400)
        else:
            return error_response(str(e), 400)

    @app.errorhandler(Exception)
    def handle_uncaught_errors(e):
        if env == "production":
            return error_response("Internal server error", 500)
        else:
            return error_response(str(e), 500)

    return app
