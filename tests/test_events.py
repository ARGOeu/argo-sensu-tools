import unittest

from argo_sensu_tools.events import PassiveEvents
from argo_sensu_tools.exceptions import ArgoSensuToolsException

PASSIVE_DATA = \
    ("[1698053882] PROCESS_SERVICE_CHECK_RESULT;grid02.hep.by;"
     "eu.egi.SRM-VOLsDir-ops;0;OK - Directory successfully listed\n")

WRONG_PASSIVE_DATA = """
[1698053882] PROCESS_SERVICE_CHECK_RESULT;grid02
"""

MULTILINE_PASSIVE_DATA = \
    ("[1704796827] PROCESS_SERVICE_CHECK_RESULT;ifaece04.pic.es;"
     "ch.cern.HTCondorCE-JobSubmit-ops;2;CRITICAL - Job (0) has failed with "
     "status: Job submit result undefined, failed to parse the job ID\n"
     "=== Credentials:\n=== Job description:\n"
     "JDL([('universe', 'vanilla'), ('executable', 'hostname'), "
     "('transfer_executable', 'true'), ('output', "
     "'/var/lib/gridprobes/ops/scondor/ifaece04.pic.es/out/gridjob.out'), "
     "('error', '/var/lib/gridprobes/ops/scondor/ifaece04.pic.es/out/"
     "gridjob.err'), ('log', '/var/lib/gridprobes/ops/scondor/ifaece04.pic.es"
     "/out/gridjob.log'), ('log_xml', 'true'), ('should_transfer_files', 'YES'"
     "), ('when_to_transfer_output', 'ON_EXIT'), ('use_x509userproxy', 'true')"
     "])\n=== Job submission command:\ncondor_submit --spool --name "
     "ifaece04.pic.es --pool ifaece04.pic.es:9619 /var/lib/gridprobes/ops/"
     "scondor/ifaece04.pic.es/gridjob.j\n\nJob submit result undefined, "
     "failed to parse the job ID\n")

MULTIPLE_EVENTS_DATA = \
    ("[1704973517] PROCESS_SERVICE_CHECK_RESULT;xrootd.phy.bris.ac.uk;"
     "egi.xrootd.readwrite-Put;1;WARNING - lsdir skipped\n[1704973517] "
     "PROCESS_SERVICE_CHECK_RESULT;xrootd.phy.bris.ac.uk;"
     "egi.xrootd.readwrite-Del;1;WARNING - Del skipped")

MULTIPLE_MULTILINE_DATA = \
    ("[1704975414] PROCESS_SERVICE_CHECK_RESULT;htc-atlas-ce02.na.infn.it;"
     "ch.cern.HTCondorCE-JobSubmit-ops;0;OK - Job successfully completed\n"
     "=== ETF job log:\nTimeout limits "
     "configured were:\n=== Credentials:\nx509:\n/DC=EU/DC=EGI/C=HR/O=Robots/O="
     "SRCE/CN=Robot:argo-egi@cro-ngi.hr/CN=864597975\n/ops/Role=NULL/Capability"
     "=NULL\n\n=== Job description:\nJDL([('universe', 'vanilla'), "
     "('executable', 'hostname'), ('transfer_executable', 'true'), ('output', "
     "'/var/lib/gridprobes/ops/scondor/htc-atlas-ce02.na.infn.it/out/"
     "gridjob.out'), ('error', '/var/lib/gridprobes/ops/scondor/htc-atlas-"
     "ce02.na.infn.it/out/gridjob.err'), ('log', '/var/lib/gridprobes/ops/"
     "scondor/htc-atlas-ce02.na.infn.it/out/gridjob.log'), ('log_xml', 'true'),"
     " ('should_transfer_files', 'YES'), ('when_to_transfer_output', "
     "'ON_EXIT'), ('use_x509userproxy', 'true')])\n=== Job submission "
     "command:\ncondor_submit --spool --name htc-atlas-ce02.na.infn.it --pool "
     "htc-atlas-ce02.na.infn.it:9619 /var/lib/gridprobes/ops/scondor/htc-"
     "atlas-ce02.na.infn.it/gridjob.jdl\nSubmitting job(s).COMPLETED\n"
     "[1704973517] PROCESS_SERVICE_CHECK_RESULT;xrootd.phy.bris.ac.uk;"
     "egi.xrootd.readwrite-Del;1;WARNING - Del skipped")

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
            },
            {
                "service": "XRootD",
                "metrics": [
                    "egi.xrootd.readwrite",
                    "egi.xrootd.readwrite-Del",
                    "egi.xrootd.readwrite-Get",
                    "egi.xrootd.readwrite-Ls",
                    "egi.xrootd.readwrite-LsDir",
                    "egi.xrootd.readwrite-Put"
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
            parsed_data, [{
                "hostname": "grid02.hep.by",
                "metric": "eu.egi.SRM-VOLsDir-ops",
                "status": 0,
                "output": "OK - Directory successfully listed"
            }]
        )

    def test_parse_multiline(self):
        events = PassiveEvents(
            message=MULTILINE_PASSIVE_DATA,
            metricprofiles=METRICPROFILES,
            voname="ops",
            namespace="TEST"
        )
        parsed_data = events._parse()
        self.assertEqual(
            parsed_data, [{
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
            }]
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

    def test_parse_multiple(self):
        events = PassiveEvents(
            message=MULTIPLE_EVENTS_DATA,
            metricprofiles=METRICPROFILES,
            voname="ops",
            namespace="TEST"
        )
        parsed_data = events._parse()
        self.assertEqual(
            parsed_data, [
                {
                    "hostname": "xrootd.phy.bris.ac.uk",
                    "metric": "egi.xrootd.readwrite-Put",
                    "status": 1,
                    "output": "WARNING - lsdir skipped"
                },
                {
                    "hostname": "xrootd.phy.bris.ac.uk",
                    "metric": "egi.xrootd.readwrite-Del",
                    "status": 1,
                    "output": "WARNING - Del skipped"
                }
            ]
        )

    def test_parse_multiple_multiline(self):
        events = PassiveEvents(
            message=MULTIPLE_MULTILINE_DATA,
            metricprofiles=METRICPROFILES,
            voname="ops",
            namespace="TEST"
        )
        parsed_data = events._parse()
        self.assertEqual(
            parsed_data, [
                {
                    "hostname": "htc-atlas-ce02.na.infn.it",
                    "metric": "ch.cern.HTCondorCE-JobSubmit-ops",
                    "status": 0,
                    "output":
                        "OK - Job successfully completed\n=== ETF job log:"
                        "\nTimeout limits configured were:\n=== Credentials:\n"
                        "x509:\n/DC=EU/DC=EGI/C=HR/O=Robots/O=SRCE/CN=Robot:"
                        "argo-egi@cro-ngi.hr/CN=864597975\n/ops/Role=NULL/"
                        "Capability=NULL\n\n=== Job description:\nJDL(["
                        "('universe', 'vanilla'), ('executable', 'hostname'), "
                        "('transfer_executable', 'true'), ('output', "
                        "'/var/lib/gridprobes/ops/scondor/htc-atlas-ce02.na."
                        "infn.it/out/gridjob.out'), ('error', '/var/lib/"
                        "gridprobes/ops/scondor/htc-atlas-ce02.na.infn.it/out/"
                        "gridjob.err'), ('log', '/var/lib/gridprobes/ops/"
                        "scondor/htc-atlas-ce02.na.infn.it/out/gridjob.log'), "
                        "('log_xml', 'true'), ('should_transfer_files', 'YES'),"
                        " ('when_to_transfer_output', 'ON_EXIT'), "
                        "('use_x509userproxy', 'true')])\n=== Job submission "
                        "command:\ncondor_submit --spool --name "
                        "htc-atlas-ce02.na.infn.it --pool "
                        "htc-atlas-ce02.na.infn.it:9619 /var/lib/gridprobes/"
                        "ops/scondor/htc-atlas-ce02.na.infn.it/gridjob.jdl\n"
                        "Submitting job(s).COMPLETED"
                },
                {
                    "hostname": "xrootd.phy.bris.ac.uk",
                    "metric": "egi.xrootd.readwrite-Del",
                    "status": 1,
                    "output": "WARNING - Del skipped"
                }
            ]
        )

    def test_create_events(self):
        events = self.events.create_events()
        self.assertEqual(events, [{
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

    def test_create_events_for_multiple_parsed(self):
        self.maxDiff = None
        passives = PassiveEvents(
            message=MULTIPLE_EVENTS_DATA,
            metricprofiles=METRICPROFILES,
            voname="ops",
            namespace="TEST"
        )
        events = passives.create_events()
        self.assertEqual(
            events, [{
                "entity": {
                    "entity_class": "proxy",
                    "metadata": {
                        "name": "XRootD__xrootd.phy.bris.ac.uk",
                        "namespace": "TEST"
                    }
                },
                "check": {
                    "output": "WARNING - lsdir skipped",
                    "status": 1,
                    "metadata": {
                        "name": "egi.xrootd.readwrite-Put"
                    },
                    "handlers": ["publisher-handler"]
                }
            }, {
                "entity": {
                    "entity_class": "proxy",
                    "metadata": {
                        "name": "XRootD__xrootd.phy.bris.ac.uk",
                        "namespace": "TEST"
                    }
                },
                "check": {
                    "output": "WARNING - Del skipped",
                    "status": 1,
                    "metadata": {
                        "name": "egi.xrootd.readwrite-Del"
                    },
                    "handlers": ["publisher-handler"]
                }
            }]
        )
