# -*- coding: utf-8 -*-
from werkzeug.local import LocalProxy
from flask import current_app

security_messages = {
    'UNAUTHORIZED': (u'您没有权限访问该页面', 'danger'),
}
