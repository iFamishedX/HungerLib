import os
import yaml
import importlib
from dataclasses import fields


def load_yaml(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def flatten_nested(data: dict) -> dict:
    """
    Flatten nested YAML into leaf-only keys.
    Section names are ignored.
    """
    flat = {}
    for key, value in data.items():
        if isinstance(value, dict):
            flat.update(flatten_nested(value))
        else:
            flat[key] = value
    return flat


def map_to_dataclass(data: dict, schema):
    """
    Map flattened dict → dataclass instance.
    Missing fields use dataclass defaults.
    """
    kwargs = {}
    for f in fields(schema):
        if f.name in data:
            kwargs[f.name] = data[f.name]
    return schema(**kwargs)


def loadConfig(path: str, default_path: str, schema):
    """
    Load a single YAML config file with fallback to defaults inside the schema's package.

    path          = runtime config path (e.g. 'config/watcher.yaml')
    default_path  = path inside the schema's package (e.g. '/defaultconfigs/watcher.yaml')
    schema        = dataclass type
    """

    # 1. Resolve runtime config path
    abs_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    # 2. Resolve default path relative to the schema's package
    module = importlib.import_module(schema.__module__)
    schema_file = os.path.abspath(module.__file__)

    # schema_file = .../serverwatcher/configmap/configclasses/watcher.py
    # package_dir = .../serverwatcher/configmap
    package_dir = os.path.dirname(os.path.dirname(schema_file))

    abs_default = os.path.join(package_dir, default_path.lstrip("/"))

    # 3. Hydrate missing runtime config
    if not os.path.exists(abs_path):
        if os.path.exists(abs_default):
            with open(abs_default, "r") as src, open(abs_path, "w") as dst:
                dst.write(src.read())
        else:
            with open(abs_path, "w") as f:
                f.write("# This file doesn't have a default!\n")

    # 4. Load + flatten + map
    raw = load_yaml(abs_path)
    flat = flatten_nested(raw)
    return map_to_dataclass(flat, schema)
