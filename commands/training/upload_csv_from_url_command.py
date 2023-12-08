from datetime import datetime
import os
import csv, string
import requests
from io import StringIO
from werkzeug.utils import secure_filename
from config import config

from commands.base_command import BaseCommand
from dao.csv_dao import csv_dao
from models.metadata.metadata_models import Source, CSVStatus

class UploadCSVFromUrlCommand(BaseCommand):

    def __init__(self, url, uploaded_by: str):
        super().__init__()
        self.url = url
        self.uploaded_by = uploaded_by
        self.csv_dao = csv_dao
        self.filename = ""

    def execute(self):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for valid response

            parsed_url = urlparse(url)
            self.filename = os.path.basename(parsed_url.path)

            csv_data = response.text  # Get the CSV data as a string
            csv_reader = csv.reader(StringIO(csv_data))

            # Check if the CSV file is in the correct format
            for row in csv_reader:
                length = len(low)
            doc_id = self.csv_dao.create_csv(self.uploaded_by, filename, url, CSVStatus.accepted, Source.icehockey)
            self.successful = True
            return doc_id
        except Exception as e:
            if self.filename:
                doc_id = self.csv_dao.create_csv(self.uploaded_by, filename, url, CSVStatus.rejected, Source.icehockey)
                self.successful = True
                return doc_id
            self.successful = False
            return False
            
