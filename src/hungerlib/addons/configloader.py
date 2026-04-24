import os
import yaml
from dataclasses import fields, is_dataclass
from typing import Any, Dict, Iterable


def ensure_yaml(path: str, default: Dict[str, Any]):
    """
    Ensure a YAML file exists at `path`.
    If missing, write `default` to it.
    """
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            yaml.dump(default, f, sort_keys=False)


def write_default_yaml(path: str, default: Dict[str, Any], overwrite: bool = False):
    """
    Explicitly write default YAML to `path`.
    If overwrite=False and file exists, do nothing.
    """
    if not overwrite and os.path.exists(path):
        return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(default, f, sort_keys=False)


def load_yaml(path: str) -> Dict[str, Any]:
    """
    Load a YAML file into a dict. Returns {} if empty.
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return data or {}


def map_to_dataclass(mapping: Dict[str, Any], schema: type):
    """
    Map a dict into a dataclass, filling missing fields with defaults.
    """
    if not is_dataclass(schema):
        raise TypeError("schema must be a dataclass type")

    kwargs = {}
    for f in fields(schema):
        kwargs[f.name] = mapping.get(f.name, f.default)
    return schema(**kwargs)


def validate_required_keys(
    mapping: Dict[str, Any],
    required: Iterable[str],
    context: str,
) -> list[str]:
    """
    Validate that all required keys exist in mapping.
    Returns list of error strings (empty if OK).
    """
    errors = []
    for key in required:
        if key not in mapping:
            errors.append(f"[{context}] Missing required key: '{key}'")
    return errors
