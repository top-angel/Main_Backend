import qrcode
from PIL import Image
import os
from config import config
from dao.qrcode_dao import qrcode_dao
from dao.batch_dao import batch_dao
from models.metadata.metadata_models import Source
def generate_qr_code(public_address, product_id, batch_name, batch_size):
    batch_dao.create_batch(public_address,product_id,batch_name,batch_size, bounty_id=None)
    for item_number in range(1, int(batch_size) + 1):
        dir_path = os.path.join(
                os.path.abspath(os.curdir),
                config["application"]["upload_folder"], "generated_qr_code"
            )
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # Construct the content string with product_name, batch_name, and counter
        content = f"Product: {product_id}\nBatch: {batch_name}\nItem: {item_number}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=50,
            border=2,
        )
        qr.add_data(content)
        qr.make(fit=True)

        # Create a QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image
        qr_code_filename = f"{public_address}_{product_id}_{batch_name}_{batch_size}_qr_code_{item_number}.png"
        filepath = os.path.join(dir_path, qr_code_filename)
        qr_img.save(filepath)
        qrcode_dao.create_qrcode(public_address, product_id, batch_name, content, filepath, None, Source.recyclium)
    return filepath

