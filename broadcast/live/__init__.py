# -*- coding:utf-8 -*-

import logging
from flask import Flask, render_template, redirect, url_for, _request_ctx_stack, \
    request, abort, session
from flask.ext.security import Security, SQLAlchemyUserDatastore
from .utils import CustomJSONEncoder
from .models import db, User, Role
from .messages import security_messages
# from flask_session import Session
import os

def _log_config(app):
    if not app.debug and not app.testing:
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            app.config.get('LOGGING_PATH'),
            maxBytes=app.config.get('LOGGING_SIZE'))
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


def create_app(config):
    app = Flask(
        __name__,
        template_folder="../dist/",
        static_folder="static/",
        static_url_path="/static")
    app.config.from_object(config)

    for key, value in security_messages.items():
        app.config['SECURITY_MSG_' + key] = value
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = os.urandom(24)
    # Session(app)
    _log_config(app)

    app.db = db
    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    app.user_datastore = user_datastore


    @app.route('/')
    def to_app():
        return redirect(url_for('ngapp.home'))

    @app.route('/_uploads/photos/<path:path>')
    def do_not_allow_uploads(path):
        return abort(404)

    from .response import init as response_init
    response_init(app)

    import ngapp
    app.register_blueprint(ngapp.bp)

    @app.before_request
    def populate_user():
        header_key = app.config.get('SECURITY_TOKEN_AUTHENTICATION_HEADER', 'Authentication-Token')
        args_key = app.config.get('SECURITY_TOKEN_AUTHENTICATION_KEY', 'token')
        header_token = request.headers.get(header_key, None)
        token = request.args.get(args_key, header_token)
        if request.get_json(silent=True):
            token = request.json.get(args_key, token)

        if token:
            user = app.extensions['security'].login_manager.token_callback(token)
            _request_ctx_stack.top.user = user

    return app
