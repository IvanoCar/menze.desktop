from flask import Flask
from app.modules.utils import essentials, utility, config
from app.modules.api_client.client import Client
import os
import sys
import logging


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

template_folder = resource_path('templates')
static_folder = resource_path('static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.config.from_object(config.Config)

os.environ['WERKZEUG_RUN_MAIN'] = 'true'
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

keys = {
    "client_id": "64b29bbae09b4ff49f8eddda1949dbdc",
    "api-keys": {
            'GET':'d5616885cb5a4e80b72b37173c854e20e1cee146926b4ad9b4abf08e09bbc19a',
            'EDIT-CREATE-DELETE':'38d31e2f0997401984e8a37d3592e76e9064ed3bbce8454880f17964352bea2c'
        }
}

# API_CLIENT = Client('http://127.0.0.1:5000', keys)
API_CLIENT = Client('https://menzeapi.herokuapp.com', keys)
ESSENTIALS = essentials.Essentials()

from app.modules.database import database

DATABASE = database.Database()

from app.modules.login.routes import login_mod
from app.modules.dashboard.routes import dash
from app.modules.processing.routes import processing_mod

app.register_blueprint(login_mod)
app.register_blueprint(dash)
app.register_blueprint(processing_mod)
