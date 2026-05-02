import inspect
import os
import yaml
import importlib
from dataclasses import fields

class Namespace:
    def __init__(self):
        pass

def deep_get(data, path):
    parts = path.split(".")
    cur = data
    for p in parts:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(p)
        if cur is None:
            return None
    return cur

def ensure_nested(obj, dotted_name):
    parts = dotted_name.split(".")
    cur = obj
    for p in parts[:-1]:
        if not hasattr(cur, p):
            setattr(cur, p, Namespace())
        cur = getattr(cur, p)
    return cur, parts[-1]

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

def loadConfig(path, default_path, schema):
    abs_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    module = importlib.import_module(schema.__module__)
    schema_file = os.path.abspath(module.__file__)
    package_dir = os.path.dirname(os.path.dirname(schema_file))
    abs_default = os.path.join(package_dir, default_path.lstrip("/"))

    if not os.path.exists(abs_path):
        if os.path.exists(abs_default):
            with open(abs_default, "r") as src, open(abs_path, "w") as dst:
                dst.write(src.read())
        else:
            with open(abs_path, "w") as f:
                f.write("# No default config found.\n")

    raw = load_yaml(abs_path)

    cfg = schema()  # empty dataclass instance

    for f in fields(schema):
        yaml_path = f.metadata.get("yaml_key")
        if not yaml_path:
            continue

        value = deep_get(raw, yaml_path)
        if value is None:
            continue

        target, attr = ensure_nested(cfg, f.name)
        setattr(target, attr, value)

    return cfg

def load():
    caller = inspect.currentframe().f_back.f_globals
    from .configloader import loadConfig
    caller["loadConfig"] = loadConfig
