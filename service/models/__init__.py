# -*- coding: utf-8 -*-
import os
from .mongodoc import Week
from mongokit import Connection

# config
MONGODB_HOST = os.getenv("REST_MONGO_HOST")
MONGODB_PORT = int(os.getenv("REST_MONGO_PORT"))

connection = Connection(MONGODB_HOST, MONGODB_PORT)
connection.register([Week])
