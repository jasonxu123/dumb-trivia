from flask import Flask
from flask_cors import CORS
from api.routes import api_routes

# purely for debugging purposes
# import os
# import sys
# print(os.environ)
# print(sys.version)

app = Flask(__name__)
# TODO: uh add some restrictions to frontend domains
CORS(app)
app.register_blueprint(api_routes, url_prefix='/api')
