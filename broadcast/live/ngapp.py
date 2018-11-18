"""Blueprint for angular js app"""
from flask import Blueprint, request, current_app, redirect, render_template
from .response import Response

bp = Blueprint(
    'ngapp', __name__,
    static_url_path='/app',
    static_folder='../dist')


@bp.route('/app/', methods=['GET'])
def home():
    return bp.send_static_file('index.html')