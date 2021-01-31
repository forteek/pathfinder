from env import variables
from app.env.UnknownEnvException import UnknownEnvException
from typing import Any, Tuple


class EnvHandler:
    def get(self, key: str) -> Any:
        try:
            return variables[key]
        except KeyError:
            raise UnknownEnvException(key)

    def list(self, *keys: str) -> Tuple:
        try:
            values = ()
            for key in keys:
                values += (variables[key],)

            return values
        except KeyError:
            raise UnknownEnvException()
