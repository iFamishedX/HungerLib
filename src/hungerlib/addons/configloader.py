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


def loadConfig(path: str, default_path: str, schema):
    """
    Load YAML config with fallback defaults and metadata-based leaf-key mapping.
    Section names are ignored entirely.
    """

    # 1. Resolve runtime config path
    abs_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    # 2. Resolve default path relative to the schema's package
    module = importlib.import_module(schema.__module__)
    schema_file = os.path.abspath(module.__file__)
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

    # 4. Load YAML and flatten it (ignore section names)
    raw = load_yaml(abs_path)
    flat = flatten_nested(raw)

    # 5. Build kwargs using metadata={"yaml_key": "..."}
    kwargs = {}
    for f in fields(schema):
        yaml_key = f.metadata.get("yaml_key")
        if yaml_key and yaml_key in flat:
            kwargs[f.name] = flat[yaml_key]

    return schema(**kwargs)
