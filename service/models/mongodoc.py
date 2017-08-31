# -*- coding: utf-8 -*-
from mongokit import Document


class Week(Document):
    """
    :class: Week

    每周空闲教室存储
    """
    __collection__ = 'weeks'
    __database__ = 'weekdb'
    structure = {
            'bno': unicode, # 楼栋号
            'weekNo': unicode, # 周号
            'mon': dict, # 这周每天的教室情况
            'tue': dict,
            'wed': dict,
            'thu': dict,
            'fri': dict
    }

    def __repr__(self):
        return '<Mongo Week bno:{} weekNo:{}>'.format(self['bno'], self['weekNo'])
