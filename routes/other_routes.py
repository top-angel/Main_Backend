import json

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from config import config
from commands.other.create_manifest import CreateManifest
from commands.other.get_public_doc import GetPublicDocument
from commands.other.notification_manager import GetPendingNotifications
from commands.query_view_command import QueryViewCommand, ViewQueryType
from commands.dataunions.litterbux.team_management import AddTeamPointCommand
from decorators.api_key_check import api_key_check
from models.db_name import DatabaseName
from models.metadata.metadata_models import EntityType, Source, EntityRewardStatus
from commands.rewards.claim_reward_command import ClaimRewardCommand
from commands.dataunions.litterbux.team_management import GetTeamStatusCommand
from commands.dataunions.litterbux.add_rewards_command import AddRewardsCommand
from dao.users_dao import user_dao

other_routes = Blueprint("other_routes", __name__)


@other_routes.route("/notifications", methods=["POST"])
@jwt_required()
def get_pending_notifications():
    public_address = get_jwt_identity()
    data = request.json
    mark_as_read = True if data.get("mark_as_read", True) is True else False
    command = GetPendingNotifications(public_address, mark_as_read=mark_as_read)
    result = command.execute()
    if command.successful:
        return jsonify(result), 200
    else:
        return jsonify({"messages": command.messages}), 400


@other_routes.route("/query-view", methods=["GET"])
@jwt_required()
def query_view():
    public_address = get_jwt_identity()
    view_name = request.args.get('view')
    design_doc = request.args.get('design-doc')
    query_type = ViewQueryType[request.args.get("query-type")]
    doc_id = request.args.get("doc_id")
    c = QueryViewCommand(public_address, DatabaseName.other, design_doc, view_name, query_type, doc_id)
    result = c.execute()
    if c.successful:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"messages": c.messages}), 400


@other_routes.route("/public-doc", methods=["GET"])
def get_public_doc():
    doc_id = request.args.get('doc_id')

    c = GetPublicDocument(doc_id)
    result = c.execute()
    if c.successful:
        return jsonify(result), 200
    else:
        return jsonify({"messages": c.messages}), 400


@other_routes.route("/create-manifest", methods=["POST"])
@jwt_required()
def create_manifest():
    public_address = get_jwt_identity()
    data = request.json

    c = CreateManifest(public_address=public_address, doc_id=data["doc_id"], data=data["data"])
    result = c.execute()
    if c.successful:
        return jsonify(result), 200
    else:
        return jsonify({"messages": c.messages}), 400


@other_routes.route("/start-tutorial", methods=["GET"])
@jwt_required()
@api_key_check()
def start_tutorial():
    public_address = get_jwt_identity()
    claims = get_jwt()

    source = Source(claims.get("source"))
    if source == Source.litterbux:
        try:
            if user_dao.get_tutorial_reward_status(public_address) == None:
                user_dao.set_tutorial_reward_claimed(public_address, EntityRewardStatus.unpaid)
                
                point = config["application"].getint("reward_start_tutorial", 10)
                reward_c = AddRewardsCommand(public_address, point)
                reward_c.execute()

                return jsonify({'result': "success"}), 200
            else:
                return jsonify({'messages': "Tutorial reward already claimed"}), 400
        except ValueError:
            return jsonify({'messages': ["Invalid json data"]}), 400
    
    return jsonify({'messages': ["Invalid source type"]}), 400


@other_routes.route("/team_status", methods=["GET"])
@jwt_required()
@api_key_check()
def get_team_status():
    public_address = get_jwt_identity()
    try:
        team_c = GetTeamStatusCommand(public_address)
        teams = team_c.execute()
        return jsonify(teams), 200
    except Exception as err:
        return jsonify({'message': ["Team Status Failure"]}), 400
