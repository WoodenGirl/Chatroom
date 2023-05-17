import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app
app = create_app()

# from eventlet import wsgi
# import eventlet
# wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)




