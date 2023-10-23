import os
import unittest

from argo_sensu_tools.passive2event import Passive2Event

PASSIVE_DATA = """
[1698053882] PROCESS_SERVICE_CHECK_RESULT;grid02.hep.by;eu.egi.SRM-VOLsDir-ops;0;OK - Directory successfully listed\n
[1698053883] PROCESS_SERVICE_CHECK_RESULT;cms-se0.kipt.kharkov.ua;eu.egi.SRM-VOPut-ops;0;OK - File was copied to SRM. Transfer time: 0:00:03.508036\n
[1698053883] PROCESS_SERVICE_CHECK_RESULT;se02.esc.qmul.ac.uk;eu.egi.SRM-VODel-ops;0;OK - File was deleted from SRM.\n
[1698053885] PROCESS_SERVICE_CHECK_RESULT;grid02.hep.by;eu.egi.SRM-VOPut-ops;0;OK - File was copied to SRM. Transfer time: 0:00:02.863600\n
"""

PASSIVE_FILE_NAME = "nagios-test.cmd"


class Passive2EventTests(unittest.TestCase):
    def setUp(self):
        with open(PASSIVE_FILE_NAME, "w") as f:
            f.write(PASSIVE_DATA)

        self.passive2event = Passive2Event(filename=PASSIVE_FILE_NAME)

    def tearDown(self):
        if os.path.isfile(PASSIVE_FILE_NAME):
            os.remove(PASSIVE_FILE_NAME)

    def test_parse_file(self):
        parsed_data = self.passive2event._parse()
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
