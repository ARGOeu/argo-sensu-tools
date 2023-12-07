import json
import unittest
from unittest import mock

from argo_sensu_tools.data import WebAPI
from argo_sensu_tools.exceptions import WebAPIException

METRICPROFILES = [
    {
        "id": "xxxx",
        "date": "2023-10-19",
        "name": "ARGO_MON_CRITICAL",
        "description": "Central ARGO-MON_CRITICAL profile",
        "services": [
            {
                "service": "org.openstack.nova",
                "metrics": [
                    "eu.egi.cloud.OpenStack-VM",
                    "org.nagios.Keystone-TCP"
                ]
            },
            {
                "service": "SRM",
                "metrics": [
                    "eu.egi.SRM-CertValidity",
                    "eu.egi.SRM-GetSURLs",
                    "eu.egi.SRM-VODel",
                    "eu.egi.SRM-VOGet",
                    "eu.egi.SRM-VOGetTurl",
                    "eu.egi.SRM-VOLs",
                    "eu.egi.SRM-VOLsDir",
                    "eu.egi.SRM-VOPut"
                ]
            },
            {
                "service": "webdav",
                "metrics": [
                    "ch.cern.WebDAV"
                ]
            }
        ]
    },
    {
        "id": "xxxx",
        "date": "2021-02-02",
        "name": "ARGO_MON_OLD",
        "description": "Central ARGO-MON profile (old version, for RHEL6).",
        "services": [
            {
                "service": "APEL",
                "metrics": [
                    "org.apel.APEL-Pub",
                    "org.apel.APEL-Sync"
                ]
            },
            {
                "service": "Central-LFC",
                "metrics": [
                    "ch.cern.LFC-Ping",
                    "ch.cern.LFC-Read",
                    "ch.cern.LFC-Write"
                ]
            },
            {
                "service": "ch.cern.dynafed",
                "metrics": [
                    "ch.cern.WebDAV-dynafed"
                ]
            }
        ]
    },
    {
        "id": "xxx",
        "date": "2023-10-23",
        "name": "ARGO_MON",
        "description": "Central ARGO-MON profile",
        "services": [
            {
                "service": "APEL",
                "metrics": [
                    "argo.APEL-Pub",
                    "argo.APEL-Sync"
                ]
            },
            {
                "service": "argo.mon",
                "metrics": [
                    "generic.certificate.validity",
                    "generic.http.connect-nagios-ui"
                ]
            },
            {
                "service": "argo.webui",
                "metrics": [
                    "org.nagios.ARGOWeb-AR",
                    "org.nagios.ARGOWeb-Status"
                ]
            }
        ]
    }
]


class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code
        self.ok = False

        if self.status_code == 200:
            self.reason = "OK"
            self.ok = True

        elif self.status_code == 401:
            self.reason = "Unauthorized"

        elif self.status_code == 500:
            self.reason = "SERVER ERROR"

    def json(self):
        if self.ok:
            return {
                "status": {
                    "message": "Success",
                    "code": "200"
                },
                "data": self.data
            }

        elif self.status_code == 401:
            return {
                "status": {
                    "message": "Unauthorized",
                    "code": "401",
                    "detail": "You need to provide a correct authentication "
                               "token using the header 'x-api-key'"
                }
            }

        else:
            return json.loads("<h1>SERVER ERROR</h1>")


class WebAPITests(unittest.TestCase):
    def setUp(self):
        self.webapi = WebAPI(
            url="https://api.devel.argo.grnet.gr",
            token="m0ck-4p1-t0k3n",
            metricprofiles=["ARGO_MON", "ARGO_MON_CRITICAL"]
        )

    @mock.patch("argo_sensu_tools.data.requests.get")
    def test_get_metricprofiles(self, mock_get):
        mock_get.return_value = MockResponse(METRICPROFILES, status_code=200)
        metricprofiles = self.webapi.get_metricprofiles()
        mock_get.assert_called_once_with(
            url="https://api.devel.argo.grnet.gr",
            headers={
                "x-api-key": "m0ck-4p1-t0k3n",
                "Accept": "application/json"
            }
        )
        self.assertEqual(
            metricprofiles, [
                {
                    "id": "xxxx",
                    "date": "2023-10-19",
                    "name": "ARGO_MON_CRITICAL",
                    "description": "Central ARGO-MON_CRITICAL profile",
                    "services": [
                        {
                            "service": "org.openstack.nova",
                            "metrics": [
                                "eu.egi.cloud.OpenStack-VM",
                                "org.nagios.Keystone-TCP"
                            ]
                        },
                        {
                            "service": "SRM",
                            "metrics": [
                                "eu.egi.SRM-CertValidity",
                                "eu.egi.SRM-GetSURLs",
                                "eu.egi.SRM-VODel",
                                "eu.egi.SRM-VOGet",
                                "eu.egi.SRM-VOGetTurl",
                                "eu.egi.SRM-VOLs",
                                "eu.egi.SRM-VOLsDir",
                                "eu.egi.SRM-VOPut"
                            ]
                        },
                        {
                            "service": "webdav",
                            "metrics": [
                                "ch.cern.WebDAV"
                            ]
                        }
                    ]
                },
                {
                    "id": "xxx",
                    "date": "2023-10-23",
                    "name": "ARGO_MON",
                    "description": "Central ARGO-MON profile",
                    "services": [
                        {
                            "service": "APEL",
                            "metrics": [
                                "argo.APEL-Pub",
                                "argo.APEL-Sync"
                            ]
                        },
                        {
                            "service": "argo.mon",
                            "metrics": [
                                "generic.certificate.validity",
                                "generic.http.connect-nagios-ui"
                            ]
                        },
                        {
                            "service": "argo.webui",
                            "metrics": [
                                "org.nagios.ARGOWeb-AR",
                                "org.nagios.ARGOWeb-Status"
                            ]
                        }
                    ]
                }
            ]
        )

    @mock.patch("argo_sensu_tools.data.requests.get")
    def test_get_metricprofiles_with_error_response(self, mock_get):
        mock_get.return_value = MockResponse(None, status_code=401)
        with self.assertRaises(WebAPIException) as context:
            self.webapi.get_metricprofiles()
        mock_get.assert_called_once_with(
            url="https://api.devel.argo.grnet.gr",
            headers={
                "x-api-key": "m0ck-4p1-t0k3n",
                "Accept": "application/json"
            }
        )
        self.assertEqual(
            context.exception.__str__(),
            "Web-API: 401 Unauthorized: You need to provide a correct "
            "authentication token using the header 'x-api-key'"
        )

    @mock.patch("argo_sensu_tools.data.requests.get")
    def test_get_metricprofiles_with_error_no_json(self, mock_get):
        mock_get.return_value = MockResponse(None, status_code=500)
        with self.assertRaises(WebAPIException) as context:
            self.webapi.get_metricprofiles()
        mock_get.assert_called_once_with(
            url="https://api.devel.argo.grnet.gr",
            headers={
                "x-api-key": "m0ck-4p1-t0k3n",
                "Accept": "application/json"
            }
        )
        self.assertEqual(
            context.exception.__str__(), "Web-API: 500 SERVER ERROR"
        )
