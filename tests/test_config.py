import os
import unittest

from argo_sensu_tools.config import Config
from argo_sensu_tools.exceptions import ConfigException

CONFIG = """
[SENSU]\n
url = https://sensu-devel.cro-ngi.hr:8080\n
token = t0k3n\n
namespace = TENANT\n
\n
[WEB-API]\n
url = https://api.devel.argo.grnet.gr\n
token = w3b-4p1-t0k3n\n
metricprofiles = ARGO_MON, ARGO_MON2
"""

FAULTY_CONFIG = """
[WEB-API]\n
url = https://api.devel.argo.grnet.gr\n
metricprofiles = ARGO_MON, ARGO_MON2
"""

CONFIG_FILE = "test.conf"
FAULTY_CONFIG_FILE = "faulty-test.conf"


class ConfigTests(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_FILE, "w") as f:
            f.write(CONFIG)

        with open(FAULTY_CONFIG_FILE, "w") as f:
            f.write(FAULTY_CONFIG)

        self.config = Config(config_file=CONFIG_FILE)
        self.faulty_config = Config(config_file=FAULTY_CONFIG_FILE)

    def tearDown(self):
        if os.path.isfile(CONFIG_FILE):
            os.remove(CONFIG_FILE)

        if os.path.isfile(FAULTY_CONFIG_FILE):
            os.remove(FAULTY_CONFIG_FILE)

    def test_get_sensu_url(self):
        self.assertEqual(
            self.config.get_sensu_url(), "https://sensu-devel.cro-ngi.hr:8080"
        )

    def test_get_sensu_url_missing_section(self):
        with self.assertRaises(ConfigException) as context:
            self.faulty_config.get_sensu_url()

        self.assertEqual(
            context.exception.__str__(),
            "Configuration error: No section: 'SENSU'"
        )

    def test_get_sensu_token(self):
        self.assertEqual(self.config.get_sensu_token(), "t0k3n")

    def test_get_namespace(self):
        self.assertEqual(self.config.get_namespace(), "TENANT")

    def test_get_webapi_url(self):
        self.assertEqual(
            self.config.get_webapi_url(), "https://api.devel.argo.grnet.gr"
        )

    def test_get_webapi_token(self):
        self.assertEqual(self.config.get_webapi_token(), "w3b-4p1-t0k3n")

    def test_get_webapi_token_missing_option(self):
        with self.assertRaises(ConfigException) as context:
            self.faulty_config.get_webapi_token()

        self.assertEqual(
            context.exception.__str__(),
            "Configuration error: No option 'token' in section: 'WEB-API'"
        )

    def test_get_metricprofiles(self):
        self.assertEqual(
            self.config.get_metricprofiles(), ["ARGO_MON", "ARGO_MON2"]
        )

    def test_missing_config_file(self):
        with self.assertRaises(ConfigException) as context:
            Config(config_file="mock.conf")

        self.assertEqual(
            context.exception.__str__(),
            "Configuration error: Missing configuration file: mock.conf"
        )
