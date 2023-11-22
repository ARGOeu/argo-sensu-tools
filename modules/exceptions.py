class ArgoSensuToolsException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class ConfigException(ArgoSensuToolsException):
    def __str__(self):
        return f"Configuration error: {str(self.msg)}"


class WebAPIException(ArgoSensuToolsException):
    def __str__(self):
        return f"Web-API: {str(self.msg)}"
