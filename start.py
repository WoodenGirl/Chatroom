from app import create_app
from eventlet import wsgi
import eventlet

app = create_app()
wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)