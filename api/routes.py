from flask import Blueprint
from datetime import datetime
from zoneinfo import ZoneInfo
from markupsafe import escape

api_routes = Blueprint('some_name', __name__)


@api_routes.route('/')
def home():
    now_str = datetime.now(ZoneInfo('US/Pacific')
                           ).isoformat(sep=' ', timespec='seconds')
    return f'Hello at this Pacific time: {now_str}'


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
