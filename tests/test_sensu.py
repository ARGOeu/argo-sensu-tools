import json
import unittest
from unittest import mock

from argo_sensu_tools.exceptions import SensuException
from argo_sensu_tools.sensu import Sensu


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code
        self.ok = False
        self.reason = ""

        if self.status_code == 201:
            self.ok = True
            self.reason = "Created"

        elif self.status_code == 400:
            self.reason = "Bad Request"

        else:
            self.reason = "Internal Server Error"


class SensuTests(unittest.TestCase):
    def setUp(self):
        self.sensu = Sensu(
            url="https://sensu-devel.cro-ngi.hr:8080",
            token="t0k3n",
            namespace="TENANT"
        )
        self.event = {
            "entity": {
                "entity_class": "proxy",
                "metadata": {
                    "name": "SRM__grid02.hep.by",
                    "namespace": "TEST"
                }
            },
            "check": {
                "output": "OK - File was copied to SRM. Transfer time: "
                          "0:00:02.863600",
                "status": 0,
                "metadata": {
                    "name": "eu.egi.SRM-VOPut"
                }
            },
            "pipelines": [
                {
                    "name": "hard_state",
                    "type": "Pipeline",
                    "api_version": "core/v2"
                }
            ]
        }

    @mock.patch("argo_sensu_tools.sensu.requests.post")
    def test_send_event(self, mock_post):
        mock_post.return_value = MockResponse(status_code=201)
        self.sensu.send_event(event=self.event)
        mock_post.assert_called_once_with(
            "https://sensu-devel.cro-ngi.hr:8080/api/core/v2/namespaces/"
            "TENANT/events",
            data=json.dumps(self.event),
            headers={
                "Authorization": "Key t0k3n",
                "Content-Type": "application/json"
            }
        )

    @mock.patch("argo_sensu_tools.sensu.requests.post")
    def test_send_event_with_error(self, mock_post):
        mock_post.return_value = MockResponse(status_code=400)
        with self.assertRaises(SensuException) as context:
            self.sensu.send_event(self.event)

        mock_post.assert_called_once_with(
            "https://sensu-devel.cro-ngi.hr:8080/api/core/v2/namespaces/"
            "TENANT/events",
            data=json.dumps(self.event),
            headers={
                "Authorization": "Key t0k3n",
                "Content-Type": "application/json"
            }
        )

        self.assertEqual(
            context.exception.__str__(),
            "Sensu error: 400 Bad Request"
        )
