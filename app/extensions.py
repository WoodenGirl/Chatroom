from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_moment import Moment
from flask_caching import Cache
from flask_assets import Environment

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(logger=True, engineio_logger=True)
moment = Moment()
login_manager = LoginManager()
cache = Cache()
asserts = Environment()

@login_manager.user_loader
def load_user(id):
    from app.models import User
    return User.query.get(int(id))

login_manager.login_view = 'auth.login'