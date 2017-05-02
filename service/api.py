# -*- coding: utf-8 -*-
import os
import sys
import json
from flask import request, jsonify, Blueprint
from .models import connection, Week


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
        return jsonify(classroom_list)
    except:
        return jsonify({}), 502
