import json
import logging

import requests
from argo_sensu_tools.exceptions import SensuException


class Sensu:
    def __init__(self, url, token, namespace):
        self.url = url
        self.token = token
        self.namespace = namespace
        self.logger = logging.getLogger("argo-sensu-tools.sensu")

    def get_checks(self):
        response = requests.get(
            f"{self.url}/api/core/v2/namespaces/{self.namespace}/checks",
            headers={
                "Authorization": f"Key {self.token}",
                "Content-Type": "application/json"
            }
        )

        if response.ok:
            return response.json()

        else:
            raise SensuException(
                f"Error fetching checks: {response.status_code} "
                f"{response.reason}"
            )

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
            self.logger.error(
                f"Sensu: Error sending event "
                f"{event['entity']['metadata']['name']}/"
                f"{event['check']['metadata']['name']}: "
                f"{response.status_code} {response.reason}"
            )

        else:
            self.logger.info(
                f"Sensu: Successfully sent event "
                f"{event['entity']['metadata']['name']}/"
                f"{event['check']['metadata']['name']}"
            )
