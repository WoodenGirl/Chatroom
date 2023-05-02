import click
from flask import Flask, render_template

from app.chat.chat import chat_blue
from app.auth.auth import auth_blue
from app.extensions import db, migrate, socketio, login_manager, moment
from app.models import User, Message
from app.config import Config


def create_app():
    app = Flask('Chatroom', static_folder=None)
    app.config.from_object(Config)
    
    register_extensions(app)
    register_blueprints(app)
    # register_errors(app)
    register_commands(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    socketio.init_app(app) 
    login_manager.init_app(app)
    moment.init_app(app)

def register_blueprints(app):
    app.register_blueprint(chat_blue)
    app.register_blueprint(auth_blue)

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
        admin = User(nickname='Grey Li', email='admin@helloflask.com')
        admin.set_password('helloflask')
        db.session.add(admin)
        db.session.commit()

        click.echo('Generating users...')
        for i in range(10):
            user = User(nickname=fake.name())
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


