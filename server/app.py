import pathlib

from flask import Flask
from flask_cors import CORS

from src.index.client_controller import index
from src.index.api_controller import index_api
from src.common.session_and_env import env

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # acceptable for single server application
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

app.register_blueprint(index)
app.register_blueprint(index_api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=bool(env["DEBUG"]))
