import os
import sys, qrcode, json
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
from PIL import Image
from config import config
from commands.qrcode.qrcode_commands import GetQRCodebyBountyID
from models.metadata.metadata_models import Source, ReportType
from decorators.permission import requires_user_role
from models.User import UserRoleType
from dao.qrcode_dao import qrcode_dao
from dao.bounty_dao import bounty_dao

qrcode_routes = Blueprint("qrcode_routes", __name__)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

@qrcode_routes.route("/get-qrcodes", methods=["GET"])
@jwt_required()
@requires_user_role(UserRoleType.Creator)
def get_qrcodes():
    public_address = get_jwt_identity()
    bounty_id = request.args.get('bounty_id')

    c = GetQRCodebyBountyID(bounty_id)
    result = c.execute()
    if c.successful:
        return jsonify({'status': 'success', "result": result}), 200
    else:
        return jsonify({'status': 'failed','messages': c.messages}), 400
