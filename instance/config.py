import os


class Config(object):
    """Parent configuration class."""
    DEBUG = True
    CSRF_ENABLE = True
    SECRET = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    pass


class TestingConfig(Config):
    """Configurations for Testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/flashcard_test'


class ProductionConfig(Config):
    """Configurations for Production."""
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}


