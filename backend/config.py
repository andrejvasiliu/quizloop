import os


class BaseConfig:
    JWT_EXP_HOURS = int(os.getenv("JWT_EXP_HOURS", 1))
    JSON_SORT_KEYS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")


class TestingConfig(BaseConfig):
    TESTING = True
    JWT_SECRET_KEY = "test-secret"


class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # crash if missing
