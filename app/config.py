import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CATCHAT_ADMIN_EMAIL = os.getenv('CATCHAT_ADMIN_EMAIL', 'admin@helloflask.com')
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You-will-never-guess'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFCATIONS = False