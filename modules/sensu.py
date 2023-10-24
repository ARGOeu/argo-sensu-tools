import json

import requests
from argo_sensu_tools.exceptions import SensuException


class Sensu:
    def __init__(self, url, token, namespace):
        self.url = url
        self.token = token
        self.namespace = namespace

    def send_event(self, event):
        response = requests.post(
            f"{self.url}/api/core/v2/namespaces/{self.namespace}/events",
            data=json.dumps(event),
            headers={
                "Authorization": f"Key {self.token}",
                "Content-Type": "application/json"
            }
        )

        if not response.ok:
            raise SensuException(f"{response.status_code} {response.reason}")
