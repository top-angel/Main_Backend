import os
from flask import Blueprint, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import Blueprint, jsonify, request
from commands.dataunions.litterbux.guild_management import CreateGuildCommand, GetGuildByIdCommand, FetchGuildListCommand, JoinGuildCommand, LeaveGuildCommand
from commands.query_view_command import ViewQueryType, QueryViewCommand
from commands.dataunions.litterbux.rank_users_command import RankUserCommand
from decorators.api_key_check import api_key_check
from models.db_name import DatabaseName

guild_routes = Blueprint("guild_routes", __name__)


@guild_routes.route("/create", methods=["POST"])
@api_key_check()
@jwt_required()
def create_guild():
    public_address = get_jwt_identity()
    form_data = request.form

    name = form_data.get("name")
    description = form_data.get("description")
    invited_users = form_data.get('invited_users')

    if "file" not in request.files:
        resp = jsonify({"message": "No file part in the request"})
        resp.status_code = 400
        return resp
    profile_image = request.files["file"]
    
    c = CreateGuildCommand(
        public_address,
        name,
        description,
        invited_users,
        profile_image,
    )
    guild = c.execute()
    if c.successful:
        return jsonify(guild), 200
    else:
        return jsonify({'messages': c.messages}), 400


@guild_routes.route("/", methods=["GET"])
@jwt_required()
@api_key_check()
def get_guild_by_id():
    guild_id = request.args.get('guild_id', type=str)
    public_address = get_jwt_identity()

    guild_command = GetGuildByIdCommand(guild_id)
    result = guild_command.execute()

    if not guild_command.successful:
        return (
            jsonify(
                {"status": "failed", "messages": guild_command.messages}
            ),
            400,
        )
    return jsonify(result), 200

@guild_routes.route("/list", methods=["GET"])
@api_key_check()
def get_guild_list():
    
    guild_command = FetchGuildListCommand()
    result = guild_command.execute()
    if not guild_command.successful:
        return (
            jsonify(
                {"status": "failed", "messages": guild_command.messages}
            ),
            400,
        )
    return jsonify(result), 200

@guild_routes.route("/leave", methods=["GET"])
@jwt_required()
@api_key_check()
def leave_guild():
    public_address = get_jwt_identity()
    guild_id = request.args.get('guild_id', type=str)

    guild_command = LeaveGuildCommand(public_address, guild_id)
    result = guild_command.execute()
    
    if not guild_command.successful:
        return (
            jsonify(
                {"status": "failed", "messages": guild_command.messages}
            ),
            400,
        )
    return jsonify({"status": "success"}), 200

@guild_routes.route("/join", methods=["GET"])
@jwt_required()
@api_key_check()
def join_guild():
    public_address = get_jwt_identity()
    guild_id = request.args.get('guild_id', type=str)

    guild_command = JoinGuildCommand(public_address, guild_id)
    result = guild_command.execute()
    
    if not guild_command.successful:
        return (
            jsonify(
                {"status": "failed", "messages": guild_command.messages}
            ),
            400,
        )
    return jsonify({"status": "success"}), 200

    
@guild_routes.route("/query-view", methods=["GET"])
@jwt_required()
@api_key_check()
def query_view():
    public_address = get_jwt_identity()
    view_name = request.args.get('view')
    design_doc = request.args.get('design-doc')
    query_type = ViewQueryType[request.args.get("query-type")]
    doc_id = request.args.get("doc_id")
    roles = get_jwt()['roles']
    c = QueryViewCommand(public_address, DatabaseName.guild_db, design_doc, view_name, query_type, doc_id, roles)
    result = c.execute()
    if c.successful:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"messages": c.messages}), 400


@guild_routes.route("/user-rank", methods=["GET"])
@api_key_check()
def get_litterbux_user_rank():
    
    rankuser_command = RankUserCommand()
    result = rankuser_command.execute()
    if not rankuser_command.successful:
        return (
            jsonify(
                {"status": "failed", "messages": rankuser_command.messages}
            ),
            400,
        )
    return jsonify(result), 200


@guild_routes.route("/get-image-by-id", methods=["GET"])
@api_key_check()
def get_image():
    args = request.args
    guild_id = args.get("id")
    guild_c = GetGuildByIdCommand(guild_id)
    guild = guild_c.execute()
    if guild_c.successful:
        image_path = guild.get("profile_image_file_path")
        if image_path:
            return send_file(image_path)
    
    return (jsonify({"status": "failed"})), 400
