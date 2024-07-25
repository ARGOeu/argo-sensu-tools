import configparser
import os

from argo_sensu_tools.exceptions import ConfigException


class Config:
    def __init__(self, config_file):
        self.file = config_file
        self._check_file_exists()
        self.config = self._read()

    def _check_file_exists(self):
        if not os.path.isfile(self.file):
            raise ConfigException(f"Missing configuration file: {self.file}")

    def _read(self):
        config = configparser.ConfigParser()
        config.read(self.file)
        return config

    @staticmethod
    def _remove_trailing_slash(url):
        if url.endswith("/"):
            url = url[:-1]

        return url

    def _read_entry(self, section, option):
        try:
            return self.config.get(section, option)

        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise ConfigException(e)

    def get_fifo(self):
        return self._read_entry("GENERAL", "fifo")

    def get_voname(self):
        return self._read_entry("GENERAL", "voname")

    def get_sensu_url(self):
        return self._remove_trailing_slash(self._read_entry("SENSU", "url"))

    def get_sensu_token(self):
        return self._read_entry("SENSU", "token")

    def get_namespace(self):
        return self._read_entry("SENSU", "namespace")

    def get_tenant(self):
        return self._read_entry("SENSU", "tenant")

    def get_webapi_url(self):
        return self._remove_trailing_slash(self._read_entry("WEB-API", "url"))

    def get_webapi_token(self):
        return self._read_entry("WEB-API", "token")

    def get_metricprofiles(self):
        metricprofiles = self._read_entry("WEB-API", "metricprofiles")
        metricprofiles = metricprofiles.split(",")
        metricprofiles = [mp.strip() for mp in metricprofiles]
        return metricprofiles
