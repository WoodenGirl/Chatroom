import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = '123Wooden'
PASSWORD = 'WO175430xihuanni^'
HOST = '123Wooden.mysql.pythonanywhere-services.com'
PORT = '3306'
DATABASE = '123Wooden$default'

class BaseConfig:
    CHATROOM_ADMIN_EMAIL = os.getenv('CHATROOM_ADMIN_EMAIL', 'admin@123Wooden.com')
    CHATROOM_MESSAGE_PER_PAGE = 30
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'my-key')
    SQLALCHEMY_TRACK_MODIFCATIONS = False
    

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    CACHE_NO_NULL_WARNING = True
    ASSETS_DEBUG = True

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    CACHE_TYPE = 'simple'

class TestingConfig(BaseConfig):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}