import os
import inspect
from typing import Any, Dict, Type

from .configloader import load_yaml, flatten_nested, map_to_dataclass

BASE_DIR = os.getcwd()
PACKAGE_DIR = os.path.dirname(__file__)

# ---------------------------------------------------------------------------
# Schema Resolver
# ---------------------------------------------------------------------------

def _discover_config_classes() -> Dict[str, Type]:
    """
    Scans hungerlib/addons/configmap/configclasses/ for dataclasses.
    Returns a mapping: filename (lowercase) -> dataclass type.
    Example:
        global.yaml -> GlobalConfig
        messages/errors.yaml -> MessagesConfig
    """
    classes = {}
    classes_dir = os.path.join(PACKAGE_DIR, "configmap", "configclasses")

    if not os.path.isdir(classes_dir):
        return classes

    for root, _, files in os.walk(classes_dir):
        for file in files:
            if not file.endswith(".py"):
                continue

            module_path = f"hungerlib.addons.configmap.configclasses.{file[:-3]}"
            try:
                module = __import__(module_path, fromlist=["*"])
            except Exception:
                continue

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    # Map class name to filename
                    classes[name.lower()] = obj

    return classes


_CONFIG_CLASSES = _discover_config_classes()


def _resolve_schema_for_file(rel_path: str) -> Type:
    """
    Given a relative YAML path like:
        messages/errors.yaml
    We try:
        - errors.yaml → ErrorsConfig
        - messages.yaml → MessagesConfig
        - global.yaml → GlobalConfig
    Matching is case-insensitive and based on class names.
    """
    base = os.path.basename(rel_path).lower()
    name_no_ext = base.replace(".yaml", "")

    # Try exact match: errors -> errorsconfig
    direct = name_no_ext + "config"
    if direct in _CONFIG_CLASSES:
        return _CONFIG_CLASSES[direct]

    # Try class named exactly like file (rare)
    if name_no_ext in _CONFIG_CLASSES:
        return _CONFIG_CLASSES[name_no_ext]

    # Fallback: GlobalConfig if present
    if "globalconfig" in _CONFIG_CLASSES:
        return _CONFIG_CLASSES["globalconfig"]

    raise KeyError(f"No schema found for config file: {rel_path}")


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_or_default(directory: str, skip_files: list[str]) -> Dict[str, Any]:
    """
    Loads all YAML files in BASE_DIR/<directory> recursively.
    Skips any file whose basename is in skip_files.
    If a file does not exist, attempts to copy from:
        PACKAGE_DIR/configmap/defaultconfigs/<directory>/<same structure>
    If no default exists, creates a placeholder YAML with:
        # This file doesn't have a default!

    Returns:
        { "relative/path.yaml": dataclass_instance }
    """
    abs_dir = os.path.join(BASE_DIR, directory)
    default_dir = os.path.join(PACKAGE_DIR, "configmap", "defaultconfigs", directory)

    # Ensure directory exists
    os.makedirs(abs_dir, exist_ok=True)

    results = {}

    # Walk user directory
    for root, _, files in os.walk(abs_dir):
        for file in files:
            if not file.endswith(".yaml"):
                continue
            if file in skip_files:
                continue

            rel_path = os.path.relpath(os.path.join(root, file), abs_dir)
            user_file = os.path.join(abs_dir, rel_path)
            default_file = os.path.join(default_dir, rel_path)

            # Ensure parent directory exists
            os.makedirs(os.path.dirname(user_file), exist_ok=True)

            # If missing, hydrate from default or create placeholder
            if not os.path.exists(user_file):
                if os.path.exists(default_file):
                    # Copy default
                    os.makedirs(os.path.dirname(user_file), exist_ok=True)
                    with open(default_file, "r") as src, open(user_file, "w") as dst:
                        dst.write(src.read())
                else:
                    # Create placeholder
                    with open(user_file, "w") as f:
                        f.write("# This file doesn't have a default!\n")

            # Load YAML
            raw = load_yaml(user_file)
            raw = flatten_nested(raw)

            # Resolve schema
            schema = _resolve_schema_for_file(rel_path)

            # Map to dataclass
            obj = map_to_dataclass(raw, schema)

            # Store
            results[rel_path] = obj

    return results
