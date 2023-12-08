import json
import logging
import os
import uuid
import zipfile

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token, get_jwt
from commands.compute.compute import CreateComputeJobInfo, GetComputeJobInfo
from commands.query_view_command import QueryViewCommand, ViewQueryType
from commands.metadata.add_annotation_command import AddAnnotationCommand
from dao.metadata_dao import image_metadata_dao
from dao.users_dao import user_dao
from models.User import UserRoleType
from models.db_name import DatabaseName
from models.metadata.metadata_models import FileLocation, Source, EntityType, EntitySubType
from config import config
from ocean_lib.example_config import ExampleConfig
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_lib.web3_internal.constants import ZERO_ADDRESS
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from eth_account.signers.local import LocalAccount
from eth_account import Account

compute_routes = Blueprint("compute_routes", __name__)


@compute_routes.route("", methods=["POST"])
@jwt_required()
def save_compute_details():
    data = json.loads(request.data)
    public_address = get_jwt_identity()
    logging.info(f"save_compute_details: [{data.get('entity_list_id')}] [{data.get('parameters')}]")
    c = CreateComputeJobInfo(public_address, data.get('entity_list_id'), data.get('parameters'))
    result = c.execute()
    if c.successful:
        return jsonify({'id': result}), 200
    else:
        return jsonify({'messages': c.messages}), 400


@compute_routes.route("/", methods=["GET"])
def query_data_for_compute():
    args = request.args
    details_id = args.get('id')
    c = GetComputeJobInfo(details_id)
    result = c.execute()
    if c.successful:
        return jsonify(result), 200
    else:
        return jsonify({'messages': c.messages}), 400


@compute_routes.route("/update-status", methods=["POST"])
@jwt_required()
def update_compute_status():
    args = request.args


@compute_routes.route("/notify-start", methods=["POST"])
@jwt_required()
def notify_compute_start():
    args = request.args


@compute_routes.route("/notify-end", methods=["POST"])
@jwt_required()
def notify_compute_end():
    args = request.args


@compute_routes.route("/data/<jwt>", methods=["GET"])
def get_data_for_compute_job(jwt):
    token = decode_token(jwt, allow_expired=True)
    roles = [UserRoleType(r) for r in token["roles"]]
    if UserRoleType.Compute_Job not in roles:
        return jsonify({"messages": [f"Api not allowed for role {roles}"]}), 400

    public_address = token["sub"]
    view_name = request.args.get('view')
    design_doc = request.args.get('design-doc')

    # query_type = ViewQueryType[request.args.get("query-type")]
    query_type = ViewQueryType.all
    doc_id = request.args.get("doc_id")
    c = QueryViewCommand(public_address, DatabaseName.metadata, design_doc, view_name, query_type, doc_id, roles,
                         attachments=False, include_docs=True)
    result = c.execute()
    if c.successful:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"messages": c.messages}), 400


@compute_routes.route("/data/download/<jwt>/<file_id>", methods=["GET"])
def download_file_by_id(jwt, file_id):
    token = decode_token(jwt, allow_expired=True)
    roles = [UserRoleType(r) for r in token["roles"]]
    if UserRoleType.Compute_Job not in roles:
        return jsonify({"messages": [f"Api not allowed for role {roles}"]}), 400

    exists, doc = image_metadata_dao.get_if_exists(file_id)
    if exists and doc["available_for_download"] is True:
        path = doc["file_path"]
        return send_file(path)
    return jsonify({"messages": "File not found"}), 400


@compute_routes.route("/data/download-zip/<jwt>", methods=["GET"])
def download_files_as_zip(jwt):
    token = decode_token(jwt, allow_expired=True)
    roles = [UserRoleType(r) for r in token["roles"]]
    if UserRoleType.Compute_Job not in roles:
        return jsonify({"messages": [f"Api not allowed for role {roles}"]}), 400

    location = request.args.get('location', FileLocation.server)
    source = token["source"]
    doc_type = EntityType(request.args.get("entity-type", type=str))
    doc_sub_type = EntitySubType(request.args.get("entity-sub-type", type=str))
    skip = request.args.get("skip", type=int, default=0)
    limit = request.args.get("limit", type=int, default=100)
    design_doc = request.args.get("design-doc", type=str, default="query-metadata")
    view_name = request.args.get("view-name", type=str, default="downloadable-docs-for-zip")

    start_key = f'["{source}","{doc_type}","{doc_sub_type}","{location}"]'
    end_key = (
        f'["{source}","{doc_type}","{doc_sub_type}","{location}",{{}}]'
    )

    result = image_metadata_dao.query_view_by_key_range(design_doc=design_doc,
                                                        view_name=view_name,
                                                        start_key=start_key,
                                                        end_key=end_key,
                                                        skip=skip,
                                                        group_level=0,
                                                        limit=limit)

    uid = str(uuid.uuid4())
    logging.info("Generated download uid %s", uid)

    storage_file_path = os.path.join("data", "cache", uid + '.zip')
    with zipfile.ZipFile(storage_file_path, 'w') as myzip:
        rows = result["rows"]
        data = [v["value"]["data"] for v in rows]

        json_f_path = os.path.join("data", "cache", uid + ".json")
        with open(json_f_path, "w") as f:
            json_object = json.dumps(data, indent=4)
            f.write(json_object)

        myzip.write(json_f_path, arcname="data.json")

        if location == FileLocation.server:
            for row in rows:
                myzip.write(row["value"]["file_path"], arcname=row["id"])

    return send_file(storage_file_path, mimetype='zip', as_attachment=True, download_name="data.zip"), 200


@compute_routes.route("/data/download-user-data-zip/<jwt>", methods=["GET"])
def download_user_files_as_zip(jwt):
    token = decode_token(jwt, allow_expired=True)
    roles = [UserRoleType(r) for r in token["roles"]]
    if UserRoleType.Compute_Job not in roles:
        return jsonify({"messages": [f"Api not allowed for role {roles}"]}), 400

    location = request.args.get('location', FileLocation.server)
    source = token["source"]
    doc_type = EntityType(request.args.get("entity-type", type=str))
    doc_sub_type = EntitySubType(request.args.get("entity-sub-type", type=str))
    skip = request.args.get("skip", type=int, default=0)
    limit = request.args.get("limit", type=int, default=100)
    public_address = request.args.get("public_address", type=str)
    design_doc = request.args.get("design-doc", type=str, default="query-metadata")
    view_name = request.args.get("view-name", type=str, default="downloadable-docs-for-zip")

    start_key = f'["{source}","{doc_type}","{doc_sub_type}","{location}"]'
    end_key = (
        f'["{source}","{doc_type}","{doc_sub_type}","{location}",{{}}]'
    )

    result = image_metadata_dao.query_view_by_key_range(design_doc=design_doc,
                                                        view_name=view_name,
                                                        start_key=start_key,
                                                        end_key=end_key,
                                                        skip=skip,
                                                        group_level=0,
                                                        limit=limit)

    uid = str(uuid.uuid4())
    logging.info("Generated download uid %s", uid)

    storage_file_path = os.path.join("data", "cache", uid + '.zip')
    with zipfile.ZipFile(storage_file_path, 'w') as myzip:
        rows = result["rows"]
        data = [v["value"]["data"] for v in rows]

        json_f_path = os.path.join("data", "cache", uid + ".json")
        with open(json_f_path, "w") as f:
            json_object = json.dumps(data, indent=4)
            f.write(json_object)

        myzip.write(json_f_path, arcname="data.json")

        if location == FileLocation.server:
            for row in rows:
                myzip.write(row["value"]["file_path"], arcname=row["id"])

    return send_file(storage_file_path, mimetype='zip', as_attachment=True, download_name="data.zip"), 200

@compute_routes.route("/data/data-share-order-params/<jwt>", methods=["GET"])
def data_share_order_params(jwt):
    token = decode_token(jwt, allow_expired=True)
    # roles = [UserRoleType(r) for r in token["roles"]]
    # if UserRoleType.Compute_Job not in roles:
    #     return jsonify({"messages": [f"Api not allowed for role {roles}"]}), 400

    data_share_id = request.args.get("data_share_id", type=str)
    data_share = image_metadata_dao.get_doc_by_id(data_share_id)

    ocean_config = ExampleConfig.get_config(config["rewards"]["network_url"])
    ocean = Ocean(ocean_config)

    asset = ocean.assets.resolve(data_share["did"])
    initialize_args = {
        "did": asset.did,
        "service": asset.services[0],
        "consumer_address": token['sub']
    }
    data_provider = DataServiceProvider
    initialize_response = data_provider.initialize(**initialize_args)
    provider_fees = initialize_response.json()["providerFee"]

    service_index = asset.get_index_of_service(asset.services[0])

    # send gas to user only 1 time
    user_obj = user_dao.get_by_public_address(token["sub"])["result"][0]

    if user_obj.get("gas_transferred") is not True:

        logging.info("Transferring gas token to user [%s]", token['sub'])
        # now transfer some gas to user.
        amount = 0.01
        json_rpc_url = config["rewards"]["network_url"]
        web3 = Web3(HTTPProvider(json_rpc_url))
        chain_id = -1
        if config["rewards"]["network"] == "mumbai":
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            chain_id = 80001
        sender_account_private_key = config["rewards"]["account_private_key"]

        account: LocalAccount = Account.from_key(sender_account_private_key)

        nonce = web3.eth.getTransactionCount(account.address)

        assert web3.isChecksumAddress(token['sub']), f"Not a valid address: {token['sub']}"

        tx = {
            'nonce': nonce,
            'to': token['sub'],
            'value': web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'chainId': chain_id
        }

        # sign the transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=sender_account_private_key)
        tx_hash = signed_tx.hash.hex()

        # send transaction
        web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logging.info("Gas transfer: Getting transaction receipt for tx [%s]", tx_hash)

        tx_receipt = web3.eth.wait_for_transaction_receipt(signed_tx.hash.hex())
        if tx_receipt is not None and tx_receipt['status'] == 1:
            # get transaction hash
            logging.info("Gas sent to user [%s]", token["sub"])

            user_obj["gas_transferred"] = True
            user_obj["gas_transfer_tx"] = tx_hash

            user_dao.save(user_obj["_id"], user_obj)

    return {
        "data_token_address": data_share["data_token_address"],
        "provider_fees": provider_fees,
        "service_index": service_index,
        "consume_market_order_fee_address": ZERO_ADDRESS,
        "consume_market_order_fee_token": ocean.OCEAN_address,
        "consume_market_order_fee_amount": 0
    }

@compute_routes.route("/data/download-share-data-zip/<jwt>", methods=["GET"])
def download_shared_data_zip(jwt):
    token = decode_token(jwt, allow_expired=True)

    data_share_id = request.args.get("data_share_id", type=str)
    data_share = image_metadata_dao.get_doc_by_id(data_share_id)

    order_tx_hash = request.args.get('order_tx_hash', type=str)
  
    ocean_config = ExampleConfig.get_config(config["rewards"]["network_url"])

    ocean = Ocean(ocean_config)

    data_token = ocean.get_datatoken(data_share['data_token_address'])

    if order_tx_hash:
        try:
            order_tx = ocean.web3.eth.get_transaction(order_tx_hash)
            order_started_events = data_token.get_event_logs('OrderStarted', order_tx.blockNumber, order_tx.blockNumber)
            order_started_events = [order_started_events for event in order_started_events if event['args']['consumer'] == token['sub']]

            if len(order_started_events) == 0:
                return jsonify({"messages": ['You don\'t have access to download the data']}), 400

            data_share["shares"][token["sub"]]['order_tx_hash'] = order_tx_hash
            image_metadata_dao.save(data_share['_id'], data_share)
        except:
            return jsonify({"messages": ['The transaction is not indexed yet. Plesae try again']}), 400
    else:
        order_tx_hash = data_share["shares"][token["sub"]]['order_tx_hash']
        if not order_tx_hash:
            return jsonify({"messages": ['Please add `order_tx_hash` as a query param']}), 400

    location = request.args.get('location', FileLocation.server)
    source = 'brainstem'
    skip = request.args.get("skip", type=int, default=0)
    limit = request.args.get("limit", type=int, default=100)
    design_doc = request.args.get("design-doc", type=str, default="query-metadata")
    view_name = request.args.get("view-name", type=str, default="downloadable-user-docs-for-zip")

    start_key = f'["{source}","{data_share["uploaded_by"]}","{location}"]'
    end_key = (
        f'["{source}","{data_share["uploaded_by"]}","{location}",{{}}]'
    )

    result = image_metadata_dao.query_view_by_key_range(design_doc=design_doc,
                                                        view_name=view_name,
                                                        start_key=start_key,
                                                        end_key=end_key,
                                                        skip=skip,
                                                        group_level=0,
                                                        limit=limit)

    uid = str(uuid.uuid4())
    logging.info("Generated download uid %s", uid)

    storage_file_path = os.path.join("data", "cache", uid + '.zip')
    with zipfile.ZipFile(storage_file_path, 'w') as myzip:
        rows = result["rows"]
        data = [v["value"]["data"] for v in rows]

        json_f_path = os.path.join("data", "cache", uid + ".json")
        with open(json_f_path, "w") as f:
            json_object = json.dumps(data, indent=4)
            f.write(json_object)

        myzip.write(json_f_path, arcname="data.json")

        if location == FileLocation.server:
            for row in rows:
                myzip.write(row["value"]["file_path"], arcname=row["id"])

    return send_file(storage_file_path, mimetype='zip', as_attachment=True, download_name="data.zip"), 200


@compute_routes.route("/data/report-share-data/<jwt>", methods=["POST"])
def report_share_data(jwt):
    token = decode_token(jwt, allow_expired=True)

    try:
        data = json.loads(request.data)
    except ValueError as e:
        logging.exception(e)
        return jsonify({"status": "failed", "messages": ["Invalid json body"]}), 400

    data_share_id = data.get("entity_id")
    data_share = image_metadata_dao.get_doc_by_id(data_share_id)

    if not data_share:
        return jsonify({"messages": ['You don\'t have access to download the data']}), 400

    if not token['sub'] in data_share['shares']:
        return jsonify({"messages": ['You don\'t have access to download the data']}), 400

    order_tx_hash = data_share["shares"][token["sub"]]['order_tx_hash']

    if not order_tx_hash:
        return jsonify({"messages": ['You didn\'t download the data yet.']}), 400

    add_annotation_command = AddAnnotationCommand(
        token["sub"], data_share_id, data.get("annotations"), None, save_to_child_doc=True
    )
    add_annotation_command.execute()
    if add_annotation_command.successful:
        return jsonify({"status": "success"}), 200
    else:
        return (
            jsonify({"status": "failed", "messages": add_annotation_command.messages}),
            400,
        )

@compute_routes.route("/data/share-data-reports/<jwt>", methods=["GET"])
def share_data_reports(jwt):
    token = decode_token(jwt, allow_expired=True)

    data_share_id = request.args.get("data_share_id", type=str)
    data_share = image_metadata_dao.get_doc_by_id(data_share_id)

    if not data_share:
        return jsonify({"messages": ['Not Found']}), 400

    if not token['sub'] == data_share['uploaded_by']:
        return jsonify({"messages": ['You don\'t have access to this data share']}), 400

    reports = []
    for annotation_id in data_share['child_docs']:
        annotation = image_metadata_dao.get_doc_by_id(annotation_id)
        reports += annotation['annotations']

    return jsonify({"reports": reports})
