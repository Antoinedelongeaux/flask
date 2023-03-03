import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/flask/')
from gestioneos import app as application
application.secret_key = ''