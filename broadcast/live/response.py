from flask import jsonify, current_app
from flask.ext.sqlalchemy import Pagination
from sqlalchemy.exc import SQLAlchemyError


class ErrorCode(object):
    UNKNOWN = 0
    FORM_INVALID = 1
    INVALID_CREDENTIALS = 2
    USER_EXISTS = 3
    SEE_MESSAGE_FOR_DETAULS = 4
    NEED_TO_RESET_PASSWORD = 5


class Response(object):

    @staticmethod
    def success(data=None):
        result = {
            'status': 'success',
        }
        if data is not None:
            if isinstance(data, Pagination):
                result['data'] = {
                    'total': data.total,
                    'items': data.items
                }
            else:
                result['data'] = data
        return jsonify(result)

    @staticmethod
    def error(message, code=ErrorCode.SEE_MESSAGE_FOR_DETAULS, payload=None):
        result = {
            'status': 'error',
            'message': message,
            'code': code
        }
        if payload:
            result['payload'] = payload
        return jsonify(result)


class InvalidArgument(Exception):
    def __init__(self, message, code=ErrorCode.SEE_MESSAGE_FOR_DETAULS, payload=None):
        Exception.__init__(self)
        self.message = message
        self.code = code
        self.payload = payload

    def to_dict(self):
        rv['payload'] = self.payload
        rv['message'] = self.message
        rv['code'] = self.code
        return rv


def init(app):
    @app.errorhandler(InvalidArgument)
    def handle_invalid_argument(error):
        return Response.error(error.message, error.code, error.payload)

    @app.errorhandler(SQLAlchemyError)
    def handle_statementError(error):
        current_app.logger.warning(error)
        current_app.db.session.rollback()
        return Response.error(error)