# -*- coding: utf-8 -*-
from flask import Flask
from celery import Celery
from config import config

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True  # abc
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.from_object(config['default'])
celery = make_celery(app)

from api import api
app.register_blueprint(api, url_prefix='/api')
