import unittest

from argo_sensu_tools.events import PassiveEvents
from argo_sensu_tools.exceptions import ArgoSensuToolsException

PASSIVE_DATA = """
[1698053882] PROCESS_SERVICE_CHECK_RESULT;grid02.hep.by;eu.egi.SRM-VOLsDir-ops;0;OK - Directory successfully listed\n
"""

WRONG_PASSIVE_DATA = """
[1698053882] PROCESS_SERVICE_CHECK_RESULT;grid02
"""

MULTILINE_PASSIVE_DATA = """
[1704796827] PROCESS_SERVICE_CHECK_RESULT;ifaece04.pic.es;ch.cern.HTCondorCE-JobSubmit-ops;2;CRITICAL - Job (0) has failed with status: Job submit result undefined, failed to parse the job ID\n=== Credentials:\n=== Job description:\nJDL([('universe', 'vanilla'), ('executable', 'hostname'), ('transfer_executable', 'true'), ('output', '/var/lib/gridprobes/ops/scondor/ifaece04.pic.es/out/gridjob.out'), ('error', '/var/lib/gridprobes/ops/scondor/ifaece04.pic.es/out/gridjob.err'), ('log', '/var/lib/gridprobes/ops/scondor/ifaece04.pic.es/out/gridjob.log'), ('log_xml', 'true'), ('should_transfer_files', 'YES'), ('when_to_transfer_output', 'ON_EXIT'), ('use_x509userproxy', 'true')])\n=== Job submission command:\ncondor_submit --spool --name ifaece04.pic.es --pool ifaece04.pic.es:9619 /var/lib/gridprobes/ops/scondor/ifaece04.pic.es/gridjob.j\n\nJob submit result undefined, failed to parse the job ID\n
"""

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
            },
            {
                "service": "org.opensciencegrid.htcondorce",
                "metrics": [
                    "ch.cern.HTCondorCE-JobState",
                    "ch.cern.HTCondorCE-JobSubmit"
                ]
            }
        ]
    }
]


class Passive2EventTests(unittest.TestCase):
    def setUp(self):
        self.events = PassiveEvents(
            message=PASSIVE_DATA,
            metricprofiles=METRICPROFILES,
            voname="ops",
            namespace="TEST"
        )

    def test_parse(self):
        parsed_data = self.events._parse()
        self.assertEqual(
            parsed_data, {
                "hostname": "grid02.hep.by",
                "metric": "eu.egi.SRM-VOLsDir-ops",
                "status": 0,
                "output": "OK - Directory successfully listed"
            }
        )

    def test_parse_multiline(self):
        self.maxDiff = None
        events = PassiveEvents(
            message=MULTILINE_PASSIVE_DATA,
            metricprofiles=METRICPROFILES,
            voname="ops",
            namespace="TEST"
        )
        parsed_data = events._parse()
        self.assertEqual(
            parsed_data, {
                "hostname": "ifaece04.pic.es",
                "metric": "ch.cern.HTCondorCE-JobSubmit-ops",
                "status": 2,
                "output":
                    "CRITICAL - Job (0) has failed with status: Job submit "
                    "result undefined, failed to parse the job ID\n=== "
                    "Credentials:\n=== Job description:\n"
                    "JDL([('universe', 'vanilla'), ('executable', 'hostname'), "
                    "('transfer_executable', 'true'), ('output', "
                    "'/var/lib/gridprobes/ops/scondor/ifaece04.pic.es/out/"
                    "gridjob.out'), ('error', '/var/lib/gridprobes/ops/scondor/"
                    "ifaece04.pic.es/out/gridjob.err'), ('log', '/var/lib/"
                    "gridprobes/ops/scondor/ifaece04.pic.es/out/gridjob.log'), "
                    "('log_xml', 'true'), ('should_transfer_files', 'YES'), "
                    "('when_to_transfer_output', 'ON_EXIT'), "
                    "('use_x509userproxy', 'true')])\n=== Job submission "
                    "command:\ncondor_submit --spool --name ifaece04.pic.es "
                    "--pool ifaece04.pic.es:9619 /var/lib/gridprobes/ops/"
                    "scondor/ifaece04.pic.es/gridjob.j\n\n"
                    "Job submit result undefined, failed to parse the job ID"
            }
        )

    def test_parse_with_error(self):
        events = PassiveEvents(
            message=WRONG_PASSIVE_DATA,
            metricprofiles=METRICPROFILES,
            voname="ops",
            namespace="TEST"
        )
        with self.assertRaises(ArgoSensuToolsException) as context:
            events._parse()
        self.assertEqual(
            context.exception.__str__(),
            "Error parsing message '[1698053882] PROCESS_SERVICE_CHECK_RESULT;"
            "grid02'"
        )

    def test_create_event(self):
        event = self.events.create_event()
        self.assertEqual(event, [{
            "entity": {
                "entity_class": "proxy",
                "metadata": {
                    "name": "SRM__grid02.hep.by",
                    "namespace": "TEST"
                }
            },
            "check": {
                "output": "OK - Directory successfully listed",
                "status": 0,
                "metadata": {
                    "name": "eu.egi.SRM-VOLsDir"
                },
                "handlers": ["publisher-handler"]
            }
        }])
