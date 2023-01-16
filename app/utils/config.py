from typing import Any, Callable, Sequence
import toml
from sanic.config import Config, SANIC_PREFIX


class TomlConfig(Config):
    def __init__(self, path: str,
                 defaults: dict[str, str | bool | int | float | None] = None,
                 env_prefix: str | None = SANIC_PREFIX,
                 keep_alive: bool | None = None,
                 *,
                 converters: Sequence[Callable[[str], Any]] | None = None):
        super().__init__(defaults, env_prefix, keep_alive, converters=converters)
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
