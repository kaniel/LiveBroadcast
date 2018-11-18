# -*- coding:utf-8 -*-
import pytz
import calendar
from flask.json import JSONEncoder
from flask import Flask, jsonify, request, current_app
from datetime import datetime
from dateutil import parser
from .transforms import transform_sqlalchemy_obj


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset():
                    obj = obj - obj.utcoffset()
                millis = int(
                    calendar.timegm(obj.timetuple()) * 1000 +
                    obj.microsecond / 1000
                )
                return millis
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        # For sqlalchemy
        if hasattr(obj, '__tablename__'):
            return transform_sqlalchemy_obj(obj)
        return JSONEncoder.default(self, obj)


def parser_datetime(datetime_str, tz=None):
    if not datetime_str:
        return None
    local_datetime = parser.parse(datetime_str)
    if not local_datetime.utcoffset():
        if not tz:
            tz = current_app.config['DEFAULT_TIMEZONE']
        local_datetime = tz.localize(local_datetime)
    return local_datetime.astimezone(pytz.utc).replace(tzinfo=None)


def parser_local_datetime(datetime_str, tz=None):
    if not datetime_str:
        return None
    utc_datetime = parser.parse(str(datetime_str))
    if not utc_datetime.utcoffset():
        if not tz:
            utc_tz = current_app.config['UTC_TIMEZONE']
            local_tz = current_app.config['DEFAULT_TIMEZONE']
        local_datetime = utc_tz.localize(utc_datetime)
        lo = local_datetime.replace(tzinfo=pytz.utc).astimezone(utc_tz)
    return local_tz.normalize(lo).replace(tzinfo=None)
