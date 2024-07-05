import json
import logging
import unittest
from unittest import mock

from argo_sensu_tools.sensu import Sensu

LOGNAME = "argo-sensu-tools.sensu"
DUMMY_LOGGER = logging.getLogger(LOGNAME)
DUMMY_LOG = [f"INFO:{LOGNAME}:dummy"]


MOCK_CHECKS = [
    {
        "command": "/usr/lib64/nagios/plugins/storage/storage_probe.py -H "
                   "{{ .labels.hostname }} -t 300 -p egi.xrootd.readwrite "
                   "{{ .labels.e__argo_xrootd_ops_url | default \"\" }} "
                   "-X /etc/sensu/certs/userproxy.pem {{ .labels."
                   "skip_ls_dir__argo_xrootd_skip_ls_dir | default \"\" }}",
        "handlers": [],
        "high_flap_threshold": 0,
        "interval": 3600,
        "low_flap_threshold": 0,
        "publish": True,
        "runtime_assets": None,
        "subscriptions": [],
        "proxy_entity_name": "",
        "check_hooks": None,
        "stdin": False,
        "subdue": None,
        "ttl": 0,
        "timeout": 900,
        "proxy_requests": {
            "entity_attributes": [
                "entity.entity_class == 'proxy'",
                "entity.labels.egi_xrootd_readwrite == 'egi.xrootd.readwrite'"
            ],
            "splay": False,
            "splay_coverage": 0
        },
        "round_robin": False,
        "output_metric_format": "",
        "output_metric_handlers": None,
        "env_vars": None,
        "metadata": {
            "name": "egi.xrootd.readwrite",
            "namespace": "tenant",
            "labels": {
                "tenants": "TENANT"
            },
            "annotations": {
                "attempts": "3"
            },
            "created_by": "admin"
        },
        "secrets": None,
        "pipelines": [
            {
                "name": "hard_state",
                "type": "Pipeline",
                "api_version": "core/v2"
            }
        ]
    },
    {
        "command": "PASSIVE",
        "handlers": [],
        "high_flap_threshold": 0,
        "interval": 0,
        "low_flap_threshold": 0,
        "publish": False,
        "runtime_assets": None,
        "subscriptions": [
            "SRM__grid02.hep.by"
        ],
        "proxy_entity_name": "",
        "check_hooks": None,
        "stdin": False,
        "subdue": None,
        "cron": "CRON_TZ=Europe/Zagreb 0 0 31 2 *",
        "ttl": 0,
        "timeout": 900,
        "round_robin": False,
        "output_metric_format": "",
        "output_metric_handlers": None,
        "env_vars": None,
        "metadata": {
            "name": "eu.egi.SRM-VOPut",
            "namespace": "tenant",
            "labels": {
                "tenants": "TENANT"
            },
            "annotations": {
                "attempts": "4"
            },
            "created_by": "admin"
        },
        "secrets": None,
        "pipelines": [
            {
                "name": "hard_state",
                "type": "Pipeline",
                "api_version": "core/v2"
            }
        ]
    },
    {
        "command": "PASSIVE",
        "handlers": [],
        "high_flap_threshold": 0,
        "interval": 0,
        "low_flap_threshold": 0,
        "publish": False,
        "runtime_assets": None,
        "subscriptions": [
            "org.opensciencegrid.htcondorce__htc-atlas-ce02.na.infn.it",
            "org.opensciencegrid.htcondorce__ifaece04.pic.es"
        ],
        "proxy_entity_name": "",
        "check_hooks": None,
        "stdin": False,
        "subdue": None,
        "cron": "CRON_TZ=Europe/Zagreb 0 0 31 2 *",
        "ttl": 0,
        "timeout": 900,
        "round_robin": False,
        "output_metric_format": "",
        "output_metric_handlers": None,
        "env_vars": None,
        "metadata": {
            "name": "ch.cern.HTCondorCE-JobSubmit",
            "namespace": "tenant",
            "labels": {
                "tenants": "TENANT"
            },
            "annotations": {
                "attempts": "2"
            },
            "created_by": "admin"
        },
        "secrets": None,
        "pipelines": [
            {
                "name": "hard_state",
                "type": "Pipeline",
                "api_version": "core/v2"
            }
        ]
    },
    {
        "command": "PASSIVE",
        "handlers": [],
        "high_flap_threshold": 0,
        "interval": 0,
        "low_flap_threshold": 0,
        "publish": False,
        "runtime_assets": None,
        "subscriptions": [
            "XRootD__xrootd.phy.bris.ac.uk"
        ],
        "proxy_entity_name": "",
        "check_hooks": None,
        "stdin": False,
        "subdue": None,
        "cron": "CRON_TZ=Europe/Zagreb 0 0 31 2 *",
        "ttl": 0,
        "timeout": 900,
        "round_robin": False,
        "output_metric_format": "",
        "output_metric_handlers": None,
        "env_vars": None,
        "metadata": {
            "name": "egi.xrootd.readwrite-Put",
            "namespace": "tenant",
            "labels": {
                "tenants": "TENANT"
            },
            "annotations": {
                "attempts": "3"
            },
            "created_by": "admin"
        },
        "secrets": None,
        "pipelines": [
            {
                "name": "hard_state",
                "type": "Pipeline",
                "api_version": "core/v2"
            }
        ]
    },
    {
        "command": "PASSIVE",
        "handlers": [],
        "high_flap_threshold": 0,
        "interval": 0,
        "low_flap_threshold": 0,
        "publish": False,
        "runtime_assets": None,
        "subscriptions": [
            "XRootD__xrootd.phy.bris.ac.uk"
        ],
        "proxy_entity_name": "",
        "check_hooks": None,
        "stdin": False,
        "subdue": None,
        "cron": "CRON_TZ=Europe/Zagreb 0 0 31 2 *",
        "ttl": 0,
        "timeout": 900,
        "round_robin": False,
        "output_metric_format": "",
        "output_metric_handlers": None,
        "env_vars": None,
        "metadata": {
            "name": "egi.xrootd.readwrite-Del",
            "namespace": "tenant",
            "labels": {
                "tenants": "TENANT"
            },
            "annotations": {
                "attempts": "3"
            },
            "created_by": "admin"
        },
        "secrets": None,
        "pipelines": [
            {
                "name": "hard_state",
                "type": "Pipeline",
                "api_version": "core/v2"
            }
        ]
    }
]


def _log_dummy():
    DUMMY_LOGGER.info("dummy")


class MockResponse:
    def __init__(self, status_code, data=None):
        self.status_code = status_code
        self.data = data
        self.ok = False
        self.reason = ""

        if self.status_code == 201:
            self.ok = True
            self.reason = "Created"

        elif self.status_code == 400:
            self.reason = "Bad Request"

        else:
            self.reason = "Internal Server Error"

    def json(self):
        return self.data


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
                    "namespace": "TEST",
                    "labels": {
                        "tenants": "TENANT"
                    }
                }
            },
            "check": {
                "output": "OK - File was copied to SRM. Transfer time: "
                          "0:00:02.863600",
                "status": 0,
                "metadata": {
                    "name": "eu.egi.SRM-VOPut",
                    "annotations": {
                        "attempts": "4"
                    },
                    "labels": {
                        "tenants": "TENANT"
                    }
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
        with self.assertLogs(LOGNAME) as log:
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
        self.assertEqual(log.output, [
            f"INFO:{LOGNAME}:Sensu: Successfully sent event "
            f"SRM__grid02.hep.by/eu.egi.SRM-VOPut"
        ])

    @mock.patch("argo_sensu_tools.sensu.requests.post")
    def test_send_event_with_error(self, mock_post):
        mock_post.return_value = MockResponse(status_code=400)
        with self.assertLogs(LOGNAME) as log:
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
            log.output, [
                f"ERROR:{LOGNAME}:Sensu: Error sending event "
                f"SRM__grid02.hep.by/eu.egi.SRM-VOPut: 400 Bad Request"
            ]
        )

    @mock.patch("argo_sensu_tools.sensu.requests.get")
    def test_get_checks(self, mock_get):
        mock_get.return_value = MockResponse(status_code=201, data=MOCK_CHECKS)
        with self.assertLogs(LOGNAME) as log:
            _log_dummy()
            checks = self.sensu.get_checks()
        mock_get.assert_called_once_with(
            "https://sensu-devel.cro-ngi.hr:8080/api/core/v2/namespaces/"
            "TENANT/checks",
            headers={
                "Authorization": "Key t0k3n",
                "Content-Type": "application/json"
            }
        )
        self.assertEqual(checks, MOCK_CHECKS)
        self.assertEqual(log.output, DUMMY_LOG)

    @mock.patch("argo_sensu_tools.sensu.requests.get")
    def test_get_checks_with_error(self, mock_get):
        mock_get.return_value = MockResponse(status_code=400)
        with self.assertLogs(LOGNAME) as log:
            self.sensu.get_checks()
        mock_get.assert_called_once_with(
            "https://sensu-devel.cro-ngi.hr:8080/api/core/v2/namespaces/"
            "TENANT/checks",
            headers={
                "Authorization": "Key t0k3n",
                "Content-Type": "application/json"
            }
        )
        self.assertEqual(log.output, [
            f"ERROR:{LOGNAME}:Sensu: Error fetching checks: 400 Bad Request"
        ])
