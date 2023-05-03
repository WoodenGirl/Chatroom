import click, os, logging, jinja2
from flask import Flask, render_template, current_app, redirect, url_for
from flask_sqlalchemy import get_debug_queries
from flask_assets import Bundle
from logging.handlers import RotatingFileHandler
from app.chat.chat import chat_blue
from app.auth.auth import auth_blue
from app.extensions import db, migrate, socketio, login_manager, moment, cache, asserts
from app.models import User, Message
from app.config import config

class MyApp(Flask):
    def __init__(
        self, 
        import_name: str,
    ):
        Flask.__init__(self, __name__)
        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.PrefixLoader({}, delimiter = ".")
        ])
    def create_global_jinja_loader(self):
        return self.jinja_loader

    def register_blueprint(self, bp):
        Flask.register_blueprint(self, bp)
        self.jinja_loader.loaders[1].mapping[bp.name] = bp.jinja_loader


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    
    app = MyApp('Chatroom')
    app.config.from_object(config[config_name])
    
    register_extensions(app)
    register_blueprints(app)
    register_index(app)
    register_errors(app)
    register_commands(app)
    # register_request_handlers(app)
    register_asserts()
    register_logger(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app) 
    login_manager.init_app(app)
    moment.init_app(app)
    cache.__init__(app)
    asserts.__init__(app)

def register_blueprints(app):
    app.register_blueprint(chat_blue)
    app.register_blueprint(auth_blue)

def register_index(app):
    @app.route('/')
    def index():
        return redirect(url_for('chat.index'))

def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', description=e.description, code=e.code), 404
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', description='Internal Server Error', code='500'), 500

def register_commands(app):

    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--message', default=300, help='Quantity of messages, default is 300.')
    def forge(message):
        """Generate fake data."""
        import random
        from sqlalchemy.exc import IntegrityError

        from faker import Faker

        fake = Faker()

        click.echo('Initializing the database...')
        db.drop_all()
        db.create_all()

        click.echo('Forging the data...')
        admin = User(nickname='123Wooden', email='admin@123Wooden.com')
        admin.set_password('123Wooden')
        db.session.add(admin)
        db.session.commit()

        click.echo('Generating users...')
        for i in range(10):
            user = User(nickname=fake.name(), email=fake.email())
            user.set_password(fake.password())
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

        click.echo('Generating messages...')
        for i in range(10):
            message = Message(
                author=User.query.get(random.randint(1, User.query.count())),
                body=fake.sentence(),
                timestamp=fake.date_time_between('-30d', '-2d'),
            )
            db.session.add(message)

        db.session.commit()
        click.echo('Done.')
    

def register_request_handlers(app):
    @app.after_app_request
    def query_profiler(response):
        for query in get_debug_queries():
            if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
                current_app.logger.warning('Slow query:{}\nParameters:{}\nDuration:{}\nContext:{}\n'.
                                        format(query.statement, query.parameters, query.duration, query.context))
        return response

def register_asserts():
    css = Bundle('css/style.css',
                 'auth/css/auth.css',
                 'chat/css/chat.css',
                 filters='cssmin', output='gen/packed.css')
    
    js = Bundle('js/jquery.js',
                'js/socket.io.js',
                'auth/js/auth.js',
                'chat/js/chat.js',
                 filters='jsmin', output='gen/packed.js')
    asserts.register('js_all', js)
    asserts.register('css_all', css)

def register_logger(app):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
   
    file_handler = RotatingFileHandler('logs/chatroom.log', maxBytes=10 * 1024 * 1024, backupCount=20)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)