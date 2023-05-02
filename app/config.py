import os
basedir = os.path.abspath(os.path.dirname(__file__))

# DIALECT = 'mysql'
# DRIVER = 'pymysql'
# USERNAME = '123Wooden'
# PASSWORD = 'WO175430xihuanni^'
# HOST = '123Wooden.mysql.pythonanywhere-services.com'
# PORT = '3306'
# DATABASE = '123Wooden$default'



class Config(object):
    CHATROOM_ADMIN_EMAIL = os.getenv('CHATROOM_ADMIN_EMAIL', 'admin@123Wooden.com')
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You-will-never-guess'

    # 配置在Pythonanywhere的mysql中
    # DATABASE_URL = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFCATIONS = False
    
    # 数据库查询分析
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 1000

    # 设置缓存
    CACHE_NO_NULL_WARNING = True
    # CACHE_TYPE = simple

    # ASSETS_DEBUG = True