import json
import datetime
from config import config
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from commands.query_view_command import ViewQueryType, QueryViewCommand
from commands.rewards.calculate_reward import CalculateRewardCommand
from commands.rewards.claim_reward_command import ClaimRewardCommand
from commands.rewards.get_reward_list import GetRewardListCommand
from commands.rewards.get_total_rewards import GetTotalRewardsCommand
from commands.rewards.mission_reward_manager import MarkMissionsAsPaid
from decorators.api_key_check import api_key_check
from decorators.permission import requires_user_role
from models.User import UserRoleType
from models.db_name import DatabaseName
from models.metadata.metadata_models import EntityType, Source
from commands.dataunions.litterbux.reward_transactions import RewardTransactions
from dao.users_dao import user_dao
from commands.rewards.get_earning_over_time import GetEarningOverTimeCommand
reward_routes = Blueprint("reward_routes", __name__)


@reward_routes.route("/claim", methods=["POST"])
@jwt_required()
def claim_reward():
    public_address = get_jwt_identity()
    claims = get_jwt()
    app = request.args.get('source')

    if app is None:
        source = Source(claims.get("source"))
    else:
        source = Source(app)

    try:
        data = json.loads(request.data)
        claim_reward_c = ClaimRewardCommand(public_address, source, EntityType.from_str(data.get("entity_type")))
    except ValueError:
        return jsonify({'messages': ["Invalid json data"]}), 400

    tx_hash = claim_reward_c.execute()
    if claim_reward_c.successful:
        return jsonify({'transaction_hash': tx_hash}), 200
    else:
        return jsonify({'messages': claim_reward_c.messages}), 400


@reward_routes.route("/", methods=["GET"])
@jwt_required()
def get_reward():
    args = request.args
    public_address = get_jwt_identity()
    claims = get_jwt()
    app = args.get('source')
    include_today = args.get('include_today', default=False, type=lambda v: v.lower() == 'true')

    # delta = 1 means include rewards up to yesterday (excluding yesterday)
    # if delta = 0 means include today's rewards
    delta = 0 if include_today is True else 1

    if app is None:
        source = Source(claims.get("source"))
    else:
        source = Source(app)
        
    entity_type = None
    if source == Source.default:
        entity_type = EntityType.from_str(args.get("entity_type"))
    try:

        get_reward_c = CalculateRewardCommand(public_address, source, entity_type, delta)
        result = get_reward_c.execute()
        
    except ValueError as e:
        return jsonify({'messages': [str(e)]}), 400

    if get_reward_c.successful:
        return jsonify(result), 200
    else:
        return jsonify({'messages': get_reward_c.messages}), 400


@reward_routes.route("/list", methods=["GET"])
@jwt_required()
def get_reward_list():
    public_address = get_jwt_identity()
    try:
        args = request.args
        get_reward_list_c = GetRewardListCommand(public_address=public_address,
                                                 entity_type=EntityType.from_str(args.get("entity_type")),
                                                 page=int(args.get('page')))
        result = get_reward_list_c.execute()
        if get_reward_list_c.successful:
            return jsonify({'result': result}), 200
        else:
            return jsonify({'messages': get_reward_list_c.messages}), 400

    except ValueError as e:
        return jsonify({'messages': [str(e)]}), 400
    except NotImplementedError as e:
        return jsonify({'messages': ["NotImplementedError: Probably invalid 'entity_type'."]}), 400


@reward_routes.route("/total-rewards", methods=["GET"])
@jwt_required()
def get_total_rewards():
    public_address = get_jwt_identity()

    try:
        get_reward_list_c = GetTotalRewardsCommand(public_address=public_address)
        result = get_reward_list_c.execute()
        if get_reward_list_c.successful:
            return jsonify({'result': result}), 200
        else:
            return jsonify({'messages': get_reward_list_c.messages}), 400

    except ValueError as e:
        return jsonify({'messages': [str(e)]}), 400
    except NotImplementedError as e:
        return jsonify({'messages': ["NotImplementedError: Probably invalid 'entity_type'."]}), 400


@reward_routes.route("/query-view", methods=["GET"])
@jwt_required()
def query_view():
    public_address = get_jwt_identity()
    view_name = request.args.get('view')
    design_doc = request.args.get('design-doc')
    query_type = ViewQueryType[request.args.get("query-type")]
    doc_id = request.args.get("doc_id")
    roles = get_jwt()['roles']
    c = QueryViewCommand(public_address, DatabaseName.missions, design_doc, view_name, query_type, doc_id, roles)
    result = c.execute()
    if c.successful:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"messages": c.messages}), 400


@reward_routes.route("/mark-as-paid", methods=["POST"])
@requires_user_role(UserRoleType.reward_oracle)
def mark_as_paid():
    data = request.json
    c = MarkMissionsAsPaid(data)
    result = c.execute()
    if c.successful:
        return jsonify({'result': result}), 200
    else:
        return jsonify({'messages': c.messages}), 400


@reward_routes.route("/litterbux/status", methods=["GET"])
@jwt_required()
@api_key_check()
def get_litterbux_status():
    public_address = get_jwt_identity()
    claims = get_jwt()
    source = Source(claims.get("source"))
    calc_rewards_c = CalculateRewardCommand(public_address, source, EntityType.image, 0)
    result = calc_rewards_c.calculate_litterbux_reward_status()
    return jsonify({'result': result}), 200

@reward_routes.route("/litterbux/claim-time", methods=["GET"])
@api_key_check()
def get_litterbux_claim_time():
    target_hour = config["application"].getint("reward_claim_hour", 0)
    if target_hour > 23:
        target_hour = target_hour % 24
    current_time = datetime.datetime.now()
    next_run_time = current_time.replace(hour=target_hour, minute=0, second=0)
    
    # check if next run time already passed
    if current_time > next_run_time:
        next_run_time += datetime.timedelta(days=1)
        
    #calculate difference
    time_difference = next_run_time - current_time
    
    return jsonify({'result': time_difference.seconds}), 200

@reward_routes.route("/cron", methods=["GET"])
def cron_job():
    c = RewardTransactions()
    c.execute()
    return jsonify({'result': "successful"}), 200

@reward_routes.route("/user", methods=["GET"])
@jwt_required()
def get_earning():
    public_address = request.args.get('public_address')
    isAdmin = get_jwt().get('is_admin')
    source = get_jwt().get('source')

    if not public_address and isAdmin and source == Source.recyclium:
        return jsonify({
            'status': 'failed',
            'messages': "Missing parameters in body `public_address`",
        }), 400

    if not isAdmin:
        public_address = get_jwt_identity()

    start_date = request.args.get('start_date')
    if not start_date:
        return jsonify({
            'status': 'failed',
            'messages': "Missing parameters in body `start_date`",
        }), 400

    end_date = request.args.get('end_date')

    if not end_date:
        return jsonify({
            'status': 'failed',
            'messages': "Missing parameters in body `end_date`",
        }), 400

    calc_rewards_c = GetEarningOverTimeCommand(public_address, start_date, end_date)
    result = calc_rewards_c.execute()
    return jsonify({'result': result, 'role':get_jwt(),'public_address':public_address}), 200
