import json
import logging
import os
from enum import Enum

from commands.base_command import BaseCommand
from config import config
from dao.metadata_dao import image_metadata_dao
from datetime import datetime
import pandas as pd
from models.metadata.metadata_models import Source, EntitySubType
from models.metadata.annotations.annotation_type import AnnotationType
from commands.metadata.upload_ipfs_command import UploadIpfsCommand
from commands.metadata.file_coin_encrypt_data_command import FileCoinEncryptDataCommand


class CreateBrainStemEntityCommand(BaseCommand):
    def __init__(self, public_address: str, file_path: str, file_type: EntitySubType, media_type: str,
                 original_file_name: str, storage: str = None):
        super(CreateBrainStemEntityCommand, self).__init__(public_address)
        self.file_path = file_path
        self.source = Source.brainstem
        self.media_type = media_type
        self.file_type = file_type
        self.original_file_name = original_file_name
        self.storage = storage

    def execute(self):
        doc_id = image_metadata_dao.generate_new_doc_id()

        child_doc_id = image_metadata_dao.generate_new_doc_id()
        child_doc_id = image_metadata_dao.add_new_child_entity(child_doc_id, self.public_address, doc_id, {}, self.file_type, self.source)

        document = {
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "created_by": self.public_address,
            "file_path": "",
            "file_type": self.file_type,
            "source": self.source,
            "type": self.media_type,
            "available_for_annotation": True,
            "available_for_verification": False,
            "available_for_download": False,
            "original_file_name": self.original_file_name,
            "annotations_required": [AnnotationType.peaq_did],
            "child_docs": [child_doc_id],
            "user_submissions": {
                AnnotationType.peaq_did: []
            }
        }
        destination_path = self.file_path

        if self.storage == "ipfs":
            c = UploadIpfsCommand(self.file_path)
            result = c.execute()
            if c.successful:
                document["file_path"] = result["url"]
                document["storage"] = self.storage
        elif self.storage == "filecoin":
            f = open(self.file_path, "rb")
            c = FileCoinEncryptDataCommand(self.public_address, "filecoin", f.read())
            document["file_path"] =  c.execute()
            document["storage"] = self.storage

        if not document["file_path"]:
            upload_directory = os.path.join(config["application"]["upload_folder"], self.public_address)
            filename = os.path.basename(self.file_path)
            destination_path = os.path.join(upload_directory, doc_id + "-" + filename)
            os.rename(self.file_path, destination_path)
            document["file_path"] = destination_path
            document["storage"] = ""

        # Enhance the document
        if self.file_type == EntitySubType.over_chunk:
            df = pd.read_csv(destination_path, delim_whitespace=True)
            top_row = df.head(1)
            bottom_row = df.tail(1)

            document["start_date_time"] = ((top_row["Date"] + " " + top_row['StartTime']).astype("string")).iloc[0]
            document["stop_date_time"] = ((bottom_row["Date"] + " " + bottom_row['StopTime']).astype("string")).iloc[0]
        elif self.file_type == EntitySubType.hbr_rr:
            try:
                first_reading = next(open(destination_path, 'r')).split()

                # Read the last reading from file.
                # Last reading = line before empty line in file (as agreed with other team)
                last_reading = []
                with open(destination_path, 'r') as data:
                    for line in data:
                        if line == '\n':
                            break
                        else:
                            last_reading = line.split()

                with open(destination_path, 'r') as data:
                    document["raw"] = data.read()

                document["first_reading"] = first_reading
                document["last_reading"] = last_reading
                image_metadata_dao.save(doc_id, document)
                # image_metadata_dao.save_attachment(filename, destination_path, doc_id, self.media_type)

            except Exception as e:
                logging.exception(f"Unable to process brainstem file content [{destination_path}]", exc_info=e)
        elif self.file_type == EntitySubType.user_metadata:
            with open(destination_path, 'r') as f:
                json_content = json.load(f)
                document["user_metadata"] = json_content
                image_metadata_dao.save(doc_id, document)
        elif self.file_type == EntitySubType.heartbeat:
            document["available_for_download"] = True
            image_metadata_dao.save(doc_id, document)

        elif self.file_type == EntitySubType.summary:
            image_metadata_dao.save(doc_id, document)
        self.successful = True
        return doc_id
