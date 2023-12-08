import json
import os
from eth_account import Account
from helpers.login import Login
from utils.get_project_dir import get_project_root
import requests
from requests import Response
from dao.metadata_dao import image_metadata_dao

#BASE_URL = 'https://crab.dev.dataunion.app'
BASE_URL = 'http://localhost:8080'
#BASE_URL = 'https://brainstem.dataunion.app'

default_accounts = []
default_tokens = []

def read_default_accounts():
    path = os.path.join(get_project_root(), "tests", "account_keys.txt")
    if os.path.isfile(path):
        with open(path) as test_accounts_file:
            for line in test_accounts_file:
                account = Account.from_key(line)
                default_accounts.append(account)

def get_access_token(account):
    token = Login.register_and_login2(
        BASE_URL, account.address, account.key
    )['access_token']
    return token

def upload_file(file_name: str, file_type: str) -> Response:
    dummy_data_path = os.path.join(get_project_root(), "tests", "data")
    file_path = os.path.join(dummy_data_path, "brainstem", file_name)

    acct = default_accounts[0]

    token = get_access_token(acct)
    headers = {"Authorization": "Bearer {0}".format(token)}

    api_url = BASE_URL + "/api/v1/upload-file"

    payload = {
        "file-type": file_type,
        "storage": "filecoin"
    }

    with open(file_path, "rb") as f:
        files = [("file", (file_name, f))]

        response = requests.request(
            "POST", api_url, headers=headers, data=payload, files=files
        )
        return response

def upload_file_to_filecoin():
    # Upload summary file
    print("Uploading...")
    file_name = "summary.txt"
    file_type = "summary"
    response = upload_file(file_name, file_type)
    data = json.loads(response.text)
    if response.status_code == 200:
        file_id = data["id"]
        print("Doc ID: {}".format(file_id))
        doc = image_metadata_dao.get_doc_by_id(file_id)
        print(doc)

        return file_id
    else:
        print(data.messages)

def download_file(file_id):
    acct = default_accounts[0]
    # Download
    print("Downloading...")
    token = get_access_token(acct)
    headers = {"Authorization": "Bearer {0}".format(token)}
    api_url = f"{BASE_URL}/api/v1/metadata/{file_id}/download"

    response = requests.request(
        "GET", api_url, headers=headers
    )
    print(response.text)

read_default_accounts()
file_id = upload_file_to_filecoin()
if file_id:
    download_file(file_id)
