import os
import logging
import sys
from datetime import timedelta
from http.client import HTTPException
from logging.handlers import TimedRotatingFileHandler
from dao.userapikey_dao import userapikey_dao
from routes.mission_routes import mission_routes
from utils.get_project_dir import get_project_root

from mongo_db import initialize_db
from config import config

log_filename = os.path.join(get_project_root(), 'logs', config["logging"]["file_name"])
handler = TimedRotatingFileHandler(filename=log_filename, when="D", interval=1)
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s",
    level=config["logging"].getint("level"),
    handlers=[handler],
)


def my_handler(type, value, tb):
    logging.exception("Uncaught exception: {0}".format(str(value)))


# Install exception handler
sys.excepthook = my_handler

from flask import Flask, send_file, jsonify, render_template
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from routes.authentication_routes import authentication_routes, sessions_dao
from routes.metadata_routes import metadata_routes
from routes.staticdata import staticdata_routes
from routes.taxonomy import taxonomy_routes
from routes.challenges import challenges_routes
from routes.stats import stats_routes
from routes.rewards import reward_routes
from routes.entity_list_routes import entity_list_routes
from routes.compute import compute_routes
from routes.handshake import handshake_routes
from routes.bounty_routes import bounty_routes
from routes.other_routes import other_routes
from routes.guild_routes import guild_routes
from routes.product_routes import product_routes
from routes.qrcode_routes import qrcode_routes
from routes.material_routes import material_routes
from routes.training_routes import training_routes
from flask_swagger import swagger
from flask_api_key import APIKeyManager

app = Flask(__name__)
CORS(app)

app.config["JWT_TOKEN_LOCATION"] = ["headers"]

# MongoEngine
app.config["MONGODB_SETTINGS"] = {
    "host": f"mongodb://"
            f"{config['MONGODB']['USERNAME']}:"
            f"{config['MONGODB']['PASSWORD']}@"
            f"{config['MONGODB']['HOST']}:"
            f"{config['MONGODB']['PORT']}/{config['MONGODB']['DATABASE']}?authSource=admin"
}
initialize_db(app)


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag["info"]["version"] = config["application"]["version"]
    swag["info"]["title"] = "Crab backend"
    swag["info"]["description"] = "Backend to handle processes"
    return jsonify(swag)


app.register_blueprint(authentication_routes)
app.register_blueprint(metadata_routes)
app.register_blueprint(staticdata_routes)
app.register_blueprint(taxonomy_routes, url_prefix="/api/v1/taxonomy")
app.register_blueprint(challenges_routes, url_prefix="/api/v1/challenges")
app.register_blueprint(stats_routes, url_prefix="/api/v1/stats")
app.register_blueprint(reward_routes, url_prefix="/api/v1/rewards")
app.register_blueprint(entity_list_routes, url_prefix="/api/v1/entity-lists")
app.register_blueprint(compute_routes, url_prefix="/api/v1/compute")
app.register_blueprint(mission_routes, url_prefix="/api/v1/missions")
app.register_blueprint(bounty_routes, url_prefix="/api/v1/bounty")
app.register_blueprint(handshake_routes, url_prefix="/api/v1/handshake")
app.register_blueprint(other_routes, url_prefix="/api/v1/other")
app.register_blueprint(guild_routes, url_prefix="/api/v1/guild")
app.register_blueprint(product_routes, url_prefix="/api/v1/product")
app.register_blueprint(material_routes, url_prefix="/api/v1/material")
app.register_blueprint(qrcode_routes, url_prefix="/api/v1/qrcode")
app.register_blueprint(training_routes, url_prefix="/api/v1/training")

app.secret_key = config["application"]["secret_key"]
app.config["UPLOAD_FOLDER"] = config["application"]["upload_folder"]
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024
app.config["JWT_SECRET_KEY"] = config["application"]["jwt_secret_string"]
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    seconds=config["application"].getint("jwt_access_token_validity")
)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
    seconds=config["application"].getint("jwt_refresh_token_validity")
)

jwt = JWTManager(app)

if not os.path.exists(config["taxonomy"]["image_folder"]):
    os.makedirs(config["taxonomy"]["image_folder"])

if not os.path.exists(config["metadata"]["thumbnail_directory"]):
    os.makedirs(config["metadata"]["thumbnail_directory"])

if not os.path.exists(config["taxonomy"]["labels_folder"]):
    os.makedirs(config["taxonomy"]["labels_folder"])

if not os.path.exists(config["metadata"]["verification_images_directory"]):
    os.makedirs(config["metadata"]["verification_images_directory"])

cache_config = {
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(cache_config)
cache = Cache(app)

app.config['FLASK_API_KEY_HEADER_NAME'] = 'X-API-KEY'
app.config['FLASK_API_KEY_PREFIX'] = 'litterbux'


mgr = APIKeyManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return sessions_dao.is_blacklisted(jti)


@app.route("/version")
def version():
    return "Version: {0}".format(config["application"]["version"])


@app.route("/", methods=["GET"])
def api():
    """
    Returns index.html file
    """
    return send_file(os.path.join("public", "index.html"))

# APIKEYManager
@mgr.create_api_key_loader
def create_api_key(key_dict):
    ak = userapikey_dao.save_key(
        key_dict.get('uuid'),
        key_dict.get('label'),
        key_dict.get('hashed_key'),
        key_dict.get('friendly_uuid'),
    )

    # and finally
    return key_dict

@mgr.fetch_api_key_loader
def fetch_api_key(uuid):
    obj = userapikey_dao.get_key(uuid)
    return obj

# @app.errorhandler(Exception)
# def handle_exception(e):
#     # pass through HTTP errors
#     if isinstance(e, HTTPException):
#         return e
#
#     logging.exception(e)
#     # now you're handling non-HTTP exceptions only
#     return render_template("500_generic.html", e=e), 500


if __name__ == "__main__":
    logging.info("Starting backend")
    app.run(debug=config["application"].getboolean("debug"), host="0.0.0.0", port=config["application"]["port"])
