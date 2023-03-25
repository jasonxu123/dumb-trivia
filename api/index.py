from flask import Flask
from api.routes import api_routes

# purely for debugging purposes
# import os
# import sys
# print(os.environ)
# print(sys.version)

app = Flask(__name__)
app.register_blueprint(api_routes, url_prefix='/api')
