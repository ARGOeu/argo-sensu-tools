import json

import requests
from argo_sensu_tools.exceptions import WebAPIException


class WebAPI:
    def __init__(self, url, token, metricprofiles):
        self.url = url
        self.token = token
        self.metricprofiles = metricprofiles

    def _get_metricprofiles(self):
        response = requests.get(
            url=self.url,
            headers={"x-api-key": self.token, "Accept": "application/json"}
        )

        if response.ok:
            return response.json()["data"]

        else:
            try:
                status = response.json()["status"]
                msg = \
                    f"{status['code']} {status['message']}: {status['detail']}"

            except (json.JSONDecodeError, KeyError):
                msg = f"{response.status_code} {response.reason}"

            raise WebAPIException(msg)

    def _filter_metricprofiles(self):
        return [
            item for item in self._get_metricprofiles()
            if item["name"] in self.metricprofiles
        ]

    def get_metricprofiles(self):
        return self._filter_metricprofiles()
