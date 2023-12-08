import json

import requests

from tests.test_base import TestBase
from dao.compute_dao import compute_dao


class TestComputeJobDetails(TestBase):

    def test_create_compute_job_details(self):
        token = self.default_tokens[0]
        headers = {"Authorization": "Bearer {0}".format(token)}
        api_url = self.url + "/api/v1/compute"
        data = {
            "parameters": {'key1': 'value1'},
            "entity_list_id": "1234",
        }
        response = requests.request(
            "POST", api_url, headers=headers, data=json.dumps(data)
        )
        self.assertEqual(200, response.status_code)
        details_id = json.load(response.text)['id']
        self.assertEqual(15, len(details_id))

    def test_get_compute_job_details(self):
        details_id = compute_dao.create_compute_input("123", "abc", {'key1': 'xyz'})
        # token = self.default_tokens[0]
        # headers = {"Authorization": "Bearer {0}".format(token)}
        api_url = self.url + f"/api/v1/compute?id={details_id}"
        response = requests.request(
            "GET", api_url, headers={}, data=json.dumps({})
        )
        self.assertEqual(200, response.status_code)
        details = json.loads(response.text)
        self.assertTrue(isinstance(details, dict))

    def test_handle_invalid_fetch(self):
        api_url = self.url + f"/api/v1/compute?id=123"
        response = requests.request(
            "GET", api_url, headers={}, data=json.dumps({})
        )
        self.assertEqual(400, response.status_code)
        details = json.loads(response.text)
        self.assertListEqual([""], details["messages"])
