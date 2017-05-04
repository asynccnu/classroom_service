# -*- coding: utf-8 -*-
import os


class Config(object):
    CELERY_BROKER_URL = 'redis://@{host}:7383/0'.format(host=os.getenv('BROKER_HOST'))  # celery消息代理, redis3容器
    CELERY_RESULT_BACKEND = 'redis://@{host}:7383/0'.format(host=os.getenv('BROKER_HOST')) # celery消息存储, redis3容器


config = {
    'default': Config
}
