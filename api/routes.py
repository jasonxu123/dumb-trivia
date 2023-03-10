from flask import Blueprint
from markupsafe import escape

api_routes = Blueprint('some_name', __name__)


@api_routes.route('/')
def home():
    return 'Hello to the donut'


@api_routes.route('/about')
def about():
    return 'Meow goes the chicken'


@api_routes.route('/here/is/long/path/<end_name>')
def long_path(end_name):
    return f'Meow goes the chicken at {escape(end_name)}'


@api_routes.route('/here/is/other/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /other/
    return f'the subpath?? {escape(subpath)}'
