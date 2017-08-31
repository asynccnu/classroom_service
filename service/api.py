# -*- coding: utf-8 -*-
"""
华师匣子空闲教室表API
"""
import os
import sys
import json
import xlrd
from . import app, celery
from .models import connection, Week
from .spiders import update_sheets
from flask import request, jsonify, Blueprint, session


api = Blueprint(
        'api',
        __name__,
        )


@api.route('/classroom/get_classroom/', methods=['GET'])
def api_get_classrooom():
    """
    :function: api_get_classroom
    :args: none

    获取空闲教室表
    """
    weekno = request.args.get('weekno')
    weekday = request.args.get('weekday')
    building = request.args.get('building')

    try:
        week = connection.Week.find_one({
            'weekNo': unicode('week'+weekno),
            'bno': unicode(building)
            })
        classroom_list = week[weekday]
        return jsonify(classroom_list), 200
    except:
        return jsonify({}), 502


@api.route('/classroom/update_classroom/', methods=['POST'])
def api_update_classroom():
    """
    :function: api_update_classroom

    更新空闲教室表
    """
    table_path = os.environ.get('TABLE_PATH')
    result = update.apply_async(args=[table_path])
    return jsonify({
        'task_id': result.id
        }), 201


@api.route('/classroom/update_classroom/', methods=['GET'])
def api_updated_classroom():
    """
    :function: api_updated_classroom

    查看空闲教室表更新状态
    """
    task_id = request.args.get('task_id')
    async_res = update.AsyncResult(task_id)
    if async_res.ready():
        return jsonify({}), 202
    else:
        return jsonify({}), 204


@celery.task()
def update(table_path):
    "更新空闲教室表celery"
    data = xlrd.open_workbook(table_path)
    all_sheets = data.sheets()
    update_sheets(all_sheets, connection, Week)
    return 'updated'
