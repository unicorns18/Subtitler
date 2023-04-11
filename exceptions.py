

class NoDotEnvFile(Exception):
    def __init__(self, message):
        self.message = message

class UnknownException(Exception):
    def __init__(self, message):
        self.message = message
