import os
import sys, qrcode, json
import zbarlight
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
from PIL import Image
from config import config
from commands.product.product_commands import CreateProductCommand, GetProductById, GetMyProducts, GetAllProducts, GetMyReports, CheckExistQRCode, GenerateQRCode
from commands.metadata.get_metadata_command import GetImagesByQRCodes
from commands.qrcode.qrcode_commands import SetQRCodeStorerToCreator, ReportPDFCreation, ReportCSVCreation, GetQRCodebyBountyID, SetRewardbyQRCodeStatus
from models.metadata.metadata_models import Source, ReportType
from decorators.permission import requires_user_role
from models.User import UserRoleType
from dao.qrcode_dao import qrcode_dao
from dao.bounty_dao import bounty_dao
from dao.report_dao import report_dao
from dao.batch_dao import batch_dao
from dao.metadata_dao import image_metadata_dao
from utils.get_qr_code import get_qr_code, get_filepath
from utils.generate_qr_code import generate_qr_code
from models.metadata.metadata_models import QRCodeStatus

product_routes = Blueprint("product_routes", __name__)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

@product_routes.route("/create", methods=["POST"])
@jwt_required()
@requires_user_role(UserRoleType.Creator)
def create_product():
    public_address = get_jwt_identity()
    claims = get_jwt()
    source = Source(claims.get("source"))

    data = request.form

    dir_path = os.path.join(
        config["application"]["upload_folder"], public_address, "products"
    )
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    example_image = request.files['example_image']
    example_image_handler = Image.open(example_image)


    example_image_filename = secure_filename(example_image.filename)
    example_image_file_path = os.path.join(dir_path, example_image_filename)
    example_image_handler.save(example_image_file_path)

    c = CreateProductCommand(public_address, data.get('name'), data.get('material_type'), data.get('material_size'), example_image_file_path, source)
    result = c.execute()
    if c.successful:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"messages": c.messages}), 400


@product_routes.route("/get/<id>", methods=["GET"])
@jwt_required()
@requires_user_role(UserRoleType.Creator)
def get_product_by_id(id):
    c = GetProductById(id)
    result = c.execute()
    if c.successful:
        return jsonify({"result": result}), 200
    else:
        return jsonify({"messages": c.messages}), 400

@product_routes.route("/<id>/example_image", methods=["GET"])
def get_product_examplge_image_by_id(id):
    c = GetProductById(id)
    result = c.execute()

    if c.successful:
        full_path = result.get("example_image")
        if os.path.isfile(full_path):
            return send_file(full_path, as_attachment=True)
        else:
            return jsonify({'status': 'failed','messages': "File not found"}), 400
    else:
        return jsonify({"messages": c.messages}), 400


@product_routes.route("/my-products", methods=["GET"])
@jwt_required()
@requires_user_role(UserRoleType.Creator)
def my_products():
    public_address = get_jwt_identity()
    c = GetMyProducts(public_address)
    result = c.execute()
    if c.successful:
        return jsonify(result), 200
    else:
        return jsonify({'messages': c.messages}), 400

@product_routes.route("/all", methods=["GET"])
@jwt_required()
@requires_user_role(UserRoleType.Recyclium_Admin)
def all():
    c = GetAllProducts()
    result = c.execute()
    if c.successful:
        return jsonify(result), 200
    else:
        return jsonify({'messages': c.messages}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@product_routes.route("/upload-qrcode", methods=["POST"])
@jwt_required()
def upload_qrcode():
    
    uploaded_file = request.files.get('file')
    bounty_id = request.form.get('bounty_id') if request.form.get('bounty_id') else None
    product_id = request.form.get('product_id')
    batch_name = request.form.get('batch_name')
    
    public_address = get_jwt_identity()

    UPLOAD_FOLDER = 'qrcode_images'
    dir_path = os.path.join(
                os.path.abspath(os.curdir),
                config["application"]["upload_folder"],
                public_address, UPLOAD_FOLDER
            )
    if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        filepath = os.path.join(dir_path, filename)
        uploaded_file.save(filepath)
    
    with open(filepath, 'rb') as image_file:
        image = Image.open(filepath)
        image.load()
    
    qr_codes = zbarlight.scan_codes(['qrcode'], image)
    qr_codes = [x.decode('utf-8') for x in qr_codes]
    
    if bounty_id is not None and qrcode_dao.is_exist_qrcode(qr_codes, bounty_id):
        return jsonify({
                'status': 'failed',
                'messages': "QRCode already exist.",
            }), 400
    qrcode_id = qrcode_dao.create_qrcode(public_address, product_id, batch_name, qr_codes, filepath, bounty_id, Source.recyclium)

    return jsonify({'status': 'success', 'id' : qrcode_id}), 400

@product_routes.route("/get-aggregation-qrcode-by-bounty", methods=["POST"])
@jwt_required()
def get_aggregation_qrcode_by_bounty():
    data = json.loads(request.data)
    bounty_id = data.get('bounty_id')
    status = data.get('status')
    if not bounty_id:
            return jsonify({
                'status': 'failed',
                'messages': "Missing parameters in body `bounty_id`",
            }), 400
    qrcodes = qrcode_dao.get_qrcodes_by_bounty_id_status(bounty_id, status)
    c = GetImagesByQRCodes(qrcodes)
    image_ids = c.execute()
    return jsonify({'status': 'success', 'items': image_ids})

@product_routes.route("/get-aggregation-qrcode-by-user", methods=["POST"])
@jwt_required()
def get_aggregation_qrcode_by_user():
    data = json.loads(request.data)
    public_address = data.get('public_address')
    status = data.get('status')
    if not public_address:
            return jsonify({
                'status': 'failed',
                'messages': "Missing parameters in body `public_address`",
            }), 400
    qrcodes = qrcode_dao.get_qrcodes_by_public_address_status(public_address, status)
    c = GetImagesByQRCodes(qrcodes)
    image_ids = c.execute()
    return jsonify({'status': 'success', 'items': image_ids})

@product_routes.route("/get-qrcodes-images", methods=["POST"])
@jwt_required()
def get_qrcode_images():
    data = json.loads(request.data)
    bounty_id = data.get('bounty_id')
    if not bounty_id:
            return jsonify({
                'status': 'failed',
                'messages': "Missing parameters in body `bounty_id`",
            }), 400
    public_address = get_jwt_identity()
    qrcodes = qrcode_dao.get_qrcodes_by_public_address_bounty_id(public_address, bounty_id)
    return jsonify({'status': 'success', 'result': qrcodes})

@product_routes.route("/set-qrcodes-storer-to-creator", methods=["POST"])
@requires_user_role(UserRoleType.Creator)
@jwt_required()
def set_qrcodes_storer_to_creator():
    data = json.loads(request.data)
    bounty_id = data.get('bounty_id')
    public_address = get_jwt_identity()
    c = SetQRCodeStorerToCreator(public_address, bounty_id)
    result = c.execute()
    if c.successful:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'failed', "messages": c.messages}), 400

@product_routes.route("/check-exist-qrcode-in-bounty", methods=["POST"])
@jwt_required()
def check_exist_qrcode_in_bounty():
    public_address = get_jwt_identity()
    data = json.loads(request.data)
    qrcode = data.get("qrcode")
    bounty_id = data.get("bounty_id")
    c = CheckExistQRCode(public_address, qrcode, bounty_id)
    result = c.execute()
    if c.successful:
        return jsonify({'status': 'success', 'id' : result}), 200
    else:
        return jsonify({'status': 'failed', 'messages': c.messages}), 400

@product_routes.route("/verify-qrcodes", methods=["POST"])
@requires_user_role(UserRoleType.Storer)
@jwt_required()
def verify_qrcodes():
    data = json.loads(request.data)
    qrcodes = data.get('qrcodes')
    status = data.get('status')
    public_address = get_jwt_identity()
    print(public_address)
    if not qrcodes:
            return jsonify({
                'status': 'failed',
                'messages': "Missing parameters in body `qrcodes`",
            }), 400
    for qrcode in qrcodes:
        metadatas = image_metadata_dao.get_image_by_qrcode(qrcode)
        image_id = metadatas[0].get("_id")
        bounty_id = metadatas[0].get("bounty_id")
        qrcode_dao.set_status_by_qrcode(public_address, qrcode, status)
        c = SetRewardbyQRCodeStatus(public_address, bounty_id, image_id, status, qrcode)
        result = c.execute()
        if c.successful:
            return jsonify({'status': 'success', 'result': result }), 200
        else:
            return jsonify({'status': 'failed', "messages": result}), 400

@product_routes.route("/verify-qrcodes-recycler-transport", methods=["POST"])
@requires_user_role(UserRoleType.Recycler)
@jwt_required()
def verify_qrcodes_recycler_transport():
    data = json.loads(request.data)
    qrcodes = data.get('qrcodes')
    public_address = get_jwt_identity()
    if not qrcodes:
        return jsonify({
            'status': 'failed',
            'messages': "Missing parameters in body `qrcodes`",
        }), 400
    print(qrcodes)
    for qrcode in qrcodes:
        qrcode_data = qrcode_dao.get_qrcodes_by_qrcode(qrcode)
        print(qrcode_data[0].get("status"))
        if qrcode_data[0].get("status") != QRCodeStatus.stored:
            return jsonify({'status': 'failed', 'message': qrcode[0] + " status is not stored."}), 400
        qrcode_dao.set_status_by_qrcode(public_address, qrcode, QRCodeStatus.transport)

    return jsonify({'status': 'success'}), 200

@product_routes.route("/verify-qrcodes-recycler-qualitycheck", methods=["POST"])
@requires_user_role(UserRoleType.Recycler)
@jwt_required()
def verify_qrcodes_recycler_qualitycheck():
    data = json.loads(request.data)
    qrcodes = data.get('qrcodes')
    public_address = get_jwt_identity()
    if not qrcodes:
        return jsonify({
            'status': 'failed',
            'messages': "Missing parameters in body `qrcodes`",
        }), 400
    print(qrcodes)
    for qrcode in qrcodes:
        qrcode_data = qrcode_dao.get_qrcodes_by_qrcode(qrcode)
        print(qrcode_data[0].get("status"))
        if qrcode_data[0].get("status") != QRCodeStatus.transport:
            return jsonify({'status': 'failed', 'message': qrcode[0] + " status is not stored."}), 400
        qrcode_dao.set_status_by_qrcode(public_address, qrcode, QRCodeStatus.qualitycheck)

    return jsonify({'status': 'success'}), 200

@product_routes.route("/verify-qrcodes-recycler-recycled", methods=["POST"])
@requires_user_role(UserRoleType.Recycler)
@jwt_required()
def verify_qrcodes_recycler_recycled():
    data = json.loads(request.data)
    qrcodes = data.get('qrcodes')
    public_address = get_jwt_identity()
    if not qrcodes:
        return jsonify({
            'status': 'failed',
            'messages': "Missing parameters in body `qrcodes`",
        }), 400
    print(qrcodes)
    for qrcode in qrcodes:
        qrcode_data = qrcode_dao.get_qrcodes_by_qrcode(qrcode)
        print(qrcode_data[0].get("status"))
        if qrcode_data[0].get("status") != QRCodeStatus.qualitycheck:
            return jsonify({'status': 'failed', 'message': qrcode[0] + " status is not stored."}), 400
        qrcode_dao.set_status_by_qrcode(public_address, qrcode, QRCodeStatus.recycled)

    return jsonify({'status': 'success'}), 200
    

@product_routes.route("/report-creation", methods=["POST"])
@requires_user_role(UserRoleType.Creator)
@jwt_required()
def report_creation():
    data = json.loads(request.data)
    public_address = get_jwt_identity()
    mission_id = data.get('mission_id')
    product_id = data.get('product_id')
    batch_name = data.get('batch_name')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    filetype = data.get('filetype')

    if filetype != ReportType.pdf and filetype != ReportType.csv:
        return jsonify({'status': 'failed', "messages": "invalide filetype"}), 400
    
    if filetype == ReportType.pdf:
        c = ReportPDFCreation(public_address, mission_id, product_id, batch_name, start_date, end_date)
    else:
        c = ReportCSVCreation(public_address, mission_id, product_id, batch_name, start_date, end_date)

    result = c.execute()

    if c.successful:
        return jsonify({'status': 'success', 'result': result}), 200
    else:
        return jsonify({'status': 'failed', "messages": c.messages}), 400

@product_routes.route("/get-reports", methods=["POST"])
@jwt_required()
@requires_user_role(UserRoleType.Creator)
def get_reports():
    data = json.loads(request.data)
    public_address = get_jwt_identity()
    mission_id = data.get('mission_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    sort_by = data.get('sort_by')
    c = GetMyReports(public_address, mission_id, sort_by, start_date, end_date)
    result = c.execute()
    if c.successful:
        return jsonify({'status': 'success', "result": result}), 200
    else:
        return jsonify({'status': 'failed','messages': c.messages}), 400

@product_routes.route("/download/<string:report_id>", methods=["GET"])
@jwt_required()
@requires_user_role(UserRoleType.Creator)
def download_file(report_id):
    report = report_dao.get_doc_by_id(report_id)
    full_path = report.get("filepath")
    if os.path.isfile(full_path):
        return send_file(full_path, as_attachment=True)
    else:
        return jsonify({'status': 'failed','messages': "File not found"}), 400

@product_routes.route("/generate-qrcode", methods=["POST"])
@jwt_required()
@requires_user_role(UserRoleType.Creator)
def generate_qrcode():
    data = request.form
    public_address = get_jwt_identity()
    product_id = data.get('product_id')
    batch_name = data.get('batch_name')
    batch_size = data.get('batch_size')
    c = GenerateQRCode(public_address, product_id, batch_name, batch_size)
    result = c.execute()
    # generate_qr_code(product_name, batch_name, batch_size)
    return jsonify({'status': 'success'}), 200

@product_routes.route("/get-all-items-batch-list", methods=["POST"])
@jwt_required()
@requires_user_role(UserRoleType.Creator)
def get_batches():
    data = json.loads(request.data)
    product_id = data.get('product_id')
    page = data.get('page')
    page_size = data.get('page_size')
    skip = (page - 1)*page_size
    qrcodes = qrcode_dao.get_qrcodes_by_product_id(product_id)
    qrcodes = qrcodes.get('result')[skip:skip+(page_size if skip + page_size > len(qrcodes.get('result')) else len(qrcodes.get('result')))]
    return jsonify({'status': 'success', 'result': qrcodes}), 400

@product_routes.route("/get-not-used-batch-list", methods=["POST"])
@jwt_required()
@requires_user_role(UserRoleType.Creator)
def get_not_used_batch_list():
    data = json.loads(request.data)
    product_id = data.get('product_id')
    page = data.get('page')
    page_size = data.get('page_size')
    skip = (page - 1)*page_size
    batch_list = batch_dao.get_all_batches_not_signed_by_product_id(product_id)
    batch_list = batch_list[skip:skip+(page_size if skip + page_size > len(batch_list) else len(batch_list))]
    return jsonify({'status': 'success', 'result': batch_list}), 400

@product_routes.route("/get-all-batch-list", methods=["POST"])
@jwt_required()
@requires_user_role(UserRoleType.Creator)
def get_all_batch_list():
    data = json.loads(request.data)
    product_id = data.get('product_id')
    page = data.get('page')
    page_size = data.get('page_size')
    skip = (page - 1)*page_size
    batch_list = batch_dao.get_all_batches_by_product_id(product_id)
    batch_list = batch_list[skip:skip+(page_size if skip + page_size > len(batch_list) else len(batch_list))]
    return jsonify({'status': 'success', 'result': batch_list}), 400

@product_routes.route("/get-qrcodes", methods=["GET"])
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
