import json
from pathlib import Path
from typing import Any, List, Dict, Tuple, Type


class ConfigError(Exception):
    """Raised when configuration validation fails."""
    pass


class Config:
    def __init__(self, schema: dict, data: dict, _root_path: str = ""):
        """
        schema: dict of
            field_name -> (
                expected_type or nested_schema,
                default_value or None,
                optional custom_error_msg
            )
        data: dict loaded from config file
        _root_path: used for nested error messages
        """
        self._schema = schema
        self._data = {}
        self._root_path = _root_path  # For clearer error messages

        for field, schema_def in schema.items():
            expected_type = schema_def[0]
            default_value = schema_def[1]
            error_msg = schema_def[2] if len(schema_def) > 2 else None

            full_field_name = f"{_root_path}{field}"

            if field in data:
                value = data[field]
                self._data[field] = self._validate_field(
                    full_field_name, value, expected_type, error_msg
                )
            else:
                if default_value is None:
                    raise ConfigError(error_msg or f"Missing required field '{full_field_name}'.")
                self._data[field] = default_value

    def _validate_field(self, name: str, value: Any, expected_type: Any, error_msg: str = None):
        """Validate a single field value against expected_type."""
        # Nested schema
        if isinstance(expected_type, dict):
            if not isinstance(value, dict):
                raise ConfigError(error_msg or f"Field '{name}' must be a dict.")
            return Config(expected_type, value, _root_path=name + ".")

        # Typed list support: e.g., List[str], List[int], List[dict-schema]
        if hasattr(expected_type, "__origin__") and expected_type.__origin__ == list:
            if not isinstance(value, list):
                raise ConfigError(error_msg or f"Field '{name}' must be a list.")
            elem_type = expected_type.__args__[0]
            return [
                self._validate_field(f"{name}[{i}]", v, elem_type, error_msg)
                for i, v in enumerate(value)
            ]

        # Normal type check
        if not isinstance(value, expected_type):
            raise ConfigError(
                error_msg or f"Field '{name}' must be of type {getattr(expected_type, '__name__', str(expected_type))}."
            )
        return value

    def __getitem__(self, key):
        return self._data[key]

    def __repr__(self):
        return f"<Config {self._data}>"

    @classmethod
    def from_file(cls, schema: dict, path: str):
        config_file = Path(path)
        if not config_file.is_file():
            raise ConfigError(f"Config file '{path}' not found.")
        with open(config_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        return cls(schema, raw_data)

    @classmethod
    def load(Config, schema: dict, config_file_path: str):
        try:
            return Config.from_file(schema, config_file_path)
        except ConfigError as e:
            print(f"ERROR: Please review the config file `{config_file_path}`:\n{e}")
