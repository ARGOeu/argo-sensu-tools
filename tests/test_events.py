import os
import unittest

from argo_sensu_tools.events import PassiveEvents

PASSIVE_DATA = """
[1698053882] PROCESS_SERVICE_CHECK_RESULT;grid02.hep.by;eu.egi.SRM-VOLsDir-ops;0;OK - Directory successfully listed\n
[1698053883] PROCESS_SERVICE_CHECK_RESULT;cms-se0.kipt.kharkov.ua;eu.egi.SRM-VOPut-ops;0;OK - File was copied to SRM. Transfer time: 0:00:03.508036\n
[1698053883] PROCESS_SERVICE_CHECK_RESULT;se02.esc.qmul.ac.uk;eu.egi.SRM-VODel-ops;0;OK - File was deleted from SRM.\n
[1698053885] PROCESS_SERVICE_CHECK_RESULT;grid02.hep.by;eu.egi.SRM-VOPut-ops;0;OK - File was copied to SRM. Transfer time: 0:00:02.863600\n
"""

PASSIVE_FILE_NAME = "nagios-test.cmd"


METRICPROFILES = [
    {
        "id": "xxxxx",
        "date": "2023-09-11",
        "name": "ARGO_MON_INTERNAL",
        "description": "Metric profile containing internal metrics.",
        "services": [
            {
                "service": "argo.mon",
                "metrics": [
                    "argo.ams-publisher.mon",
                    "argo.ncg.mon",
                    "argo.oidc.refresh-token-validity",
                    "argo.oidc.token-fetch",
                    "argo.poem-tools.check",
                    "generic.dirsize.ams-publisher",
                    "generic.disk.usage-local",
                    "generic.file.nagios-cmd",
                    "generic.procs.crond",
                    "org.nordugrid.ARC-CE-clean",
                    "org.nordugrid.ARC-CE-monitor",
                    "srce.cadist.check",
                    "srce.cadist.get-files",
                    "srce.certificate.validity-local",
                    "srce.gridproxy.get",
                    "srce.gridproxy.validity",
                    "srce.nagios.good-ses"
                ]
            }
        ]
    },
    {
        "id": "xxxx",
        "date": "2023-10-19",
        "name": "ARGO_MON_CRITICAL",
        "description": "Central ARGO-MON_CRITICAL profile",
        "services": [
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
            }
        ]
    }
]


class Passive2EventTests(unittest.TestCase):
    def setUp(self):
        with open(PASSIVE_FILE_NAME, "w") as f:
            f.write(PASSIVE_DATA)

        self.events = PassiveEvents(
            filename=PASSIVE_FILE_NAME,
            metricprofiles=METRICPROFILES,
            voname="ops",
            namespace="TEST"
        )

    def tearDown(self):
        if os.path.isfile(PASSIVE_FILE_NAME):
            os.remove(PASSIVE_FILE_NAME)

    def test_parse_file(self):
        parsed_data = self.events._parse()
        self.assertEqual(
            parsed_data, [
                {
                    "hostname": "grid02.hep.by",
                    "metric": "eu.egi.SRM-VOLsDir-ops",
                    "status": 0,
                    "output": "OK - Directory successfully listed"
                },
                {
                    "hostname": "cms-se0.kipt.kharkov.ua",
                    "metric": "eu.egi.SRM-VOPut-ops",
                    "status": 0,
                    "output": "OK - File was copied to SRM. Transfer time: "
                              "0:00:03.508036"
                },
                {
                    "hostname": "se02.esc.qmul.ac.uk",
                    "metric": "eu.egi.SRM-VODel-ops",
                    "status": 0,
                    "output": "OK - File was deleted from SRM."
                },
                {
                    "hostname": "grid02.hep.by",
                    "metric": "eu.egi.SRM-VOPut-ops",
                    "status": 0,
                    "output": "OK - File was copied to SRM. Transfer time: "
                              "0:00:02.863600"
                }
            ]
        )

    def test_create_event(self):
        event = self.events._create_event({
            "hostname": "grid02.hep.by",
            "metric": "eu.egi.SRM-VOPut-ops",
            "status": 0,
            "output": "OK - File was copied to SRM. Transfer time: "
                      "0:00:02.863600"
        })
        self.assertEqual(event, [{
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
        }])
