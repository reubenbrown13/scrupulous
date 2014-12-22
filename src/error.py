class ScrupulousError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg

    def __str__(self):
        return str(self.msg)

class ConfigError(ScrupulousError):
    def __init__(self, msg):
        ScrupulousError.__init__(self, msg)

class MiscError(ScrupulousError):
    def __init__(self, msg):
        ScrupulousError.__init__(self, msg)
