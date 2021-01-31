class UnknownEnvException(Exception):
    def __init__(self, key=''):
        super().__init__('Unknown environmental variable %s requested.' % key)
