import os
import yaml
from dataclasses import fields, is_dataclass


def ensure_yaml(path: str, default: dict):
    """Create YAML file with defaults if missing."""
    if not os.path.exists(path):
        with open(path, "w") as f:
            yaml.dump(default, f, sort_keys=False)


def load_yaml(path: str) -> dict:
    """Load YAML file into dict."""
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data or {}


def map_to_dataclass(mapping: dict, schema: type):
    """Map a dict into a dataclass, filling missing fields with defaults."""
    if not is_dataclass(schema):
        raise TypeError("schema must be a dataclass type")

    kwargs = {}
    for f in fields(schema):
        kwargs[f.name] = mapping.get(f.name, f.default)
    return schema(**kwargs)
