from json import JSONEncoder


class ObjectEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
