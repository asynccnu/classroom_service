# -*- coding: utf-8 -*-
import json
import unittest
from base64 import b64encode
from flask import Flask
from service import make_celery
from service.config import config


class APITestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object(config['default'])
        celery = make_celery(app)
        from service.api import api
        app.register_blueprint(api, url_prefix='/api')
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_404(self):
        response = self.client.get(
                '/wrong/url',
                headers=self.get_api_headers('email', 'password'))
        self.assertTrue(response.status_code == 404)

    def test_get_classroom(self):
        response = self.client.get(
                '/api/classroom/get_classroom/?weekno=10&weekday=mon&building=7'
                )
        self.assertTrue(response.status_code == 200)

    def test_update_classroom(self):
        response = self.client.post(
                '/api/classroom/update_classroom/'
                )
        self.assertTrue(response.status_code == 201)
