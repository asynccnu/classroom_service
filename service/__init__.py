# -*- coding: utf-8 -*-
from flask import Flask

def create_app(config_name='default'):
    app = Flask(__name__)
    from api import api
    app.register_blueprint(api, url_prefix='/api')

    return app

app = create_app()
