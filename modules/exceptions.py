class ArgoSensuToolsException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"Error: {str(self.msg)}"


class ConfigException(ArgoSensuToolsException):
    def __str__(self):
        return f"Configuration error: {str(self.msg)}"
