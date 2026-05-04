import inspect
import os
import yaml
import importlib
from dataclasses import fields, MISSING

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

def convert_value(value, annotation):
    if annotation is int:
        return int(value)
    if annotation is float:
        return float(value)
    if annotation is bool:
        return bool(value)
    return value

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
    values = {}

    mode = getattr(schema, "__mode__", None)

    for f in fields(schema):
        # --- OLD SYSTEM SUPPORT (yaml_key) ---
        yaml_path = f.metadata.get("yaml_key") if f.metadata else None
        if yaml_path:
            value = deep_get(raw, yaml_path)
            if value is not None:
                values[f.name] = convert_value(value, f.type)
            continue

        # --- NEW SYSTEM: mode="config" + string defaults ---
        default = f.default
        if mode == "config" and isinstance(default, str):
            yaml_path = default
            value = deep_get(raw, yaml_path)
            if value is not None:
                values[f.name] = convert_value(value, f.type)
            continue

        # --- FALLBACK: use dataclass default ---
        if default is not MISSING:
            values[f.name] = default

    return schema(**values)
