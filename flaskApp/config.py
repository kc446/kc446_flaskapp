import os

class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEBUG = False
    TESTING = False
    SECRET_KEY = "This is an INSECURE secret - DO NOT use in production!"
    SESSION_COOKIE_SECURE = True
    BOOTSTRAP_BOOTSWATCH_THEME = 'Simplex'
    DB_DIR = os.getenv('DB_DIR', "database")
    SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.abspath(DB_DIR)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, '..', DB_DIR, "db.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = './uploads'
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'NOKEY')

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    SESSION_COOKIE_SECURE = False
    DEBUG = True