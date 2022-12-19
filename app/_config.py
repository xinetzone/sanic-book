from typing import Any
from sanic.config import Config
import toml


class TomlConfig(Config):
    def __init__(self, *args, path: str, **kwargs):
        super().__init__(*args, **kwargs)

        with open(path, "r", encoding="utf-8") as f:
            self.apply(toml.load(f))

    def apply(self, config):
        self.update(self._to_uppercase(config))

    def _to_uppercase(self, obj: dict[str, Any]) -> dict[str, Any]:
        retval: dict[str, Any] = {}
        for key, value in obj.items():
            upper_key = key.upper()
            if isinstance(value, list):
                retval[upper_key] = [
                    self._to_uppercase(item) for item in value
                ]
            elif isinstance(value, dict):
                retval[upper_key] = self._to_uppercase(value)
            else:
                retval[upper_key] = value
        return retval

