import re
from dataclasses import dataclass, fields, is_dataclass

_default_maps = []

def set_default_maps(*maps):
    global _default_maps
    _default_maps = list(maps)

def get_default_maps():
    return _default_maps

class Syntax:
    braces   = r"\{([^{}]+)\}"
    dollars  = r"\$\{([^{}]+)\}"
    angles   = r"<([^<>]+)>"
    percents = r"%([^%]+)%"

@dataclass
class DataMap:
    __syntax__: str = Syntax.braces
    __mode__ = None
    def as_map(self):
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if f.init and f.name not in ("__syntax__", "__mode__")
        }
    @classmethod
    def get_syntax(cls):
        return getattr(cls, "__syntax__", Syntax.braces)

def datamap(_cls=None, *, syntax=Syntax.braces, mode=None):
    def wrap(cls):
        cls.__syntax__ = syntax
        cls.__mode__ = mode

        namespace = dict(cls.__dict__)
        namespace["__dict__"] = {}

        cls = type(cls.__name__, (DataMap,), namespace)
        return dataclass(frozen=False)(cls)

    return wrap if _cls is None else wrap(_cls)

datamap.braces = datamap(syntax=Syntax.braces)
datamap.angles = datamap(syntax=Syntax.angles)
datamap.dollars = datamap(syntax=Syntax.dollars)
datamap.percents = datamap(syntax=Syntax.percents)

def mapit(text: str, *maps, only_maps=None, disable=None, enable=None, **runtime):
    # 1. FULL OVERRIDE MODE
    if only_maps is not None:
        maps_to_use = list(only_maps)

    else:
        # 2. Start with default maps
        maps_to_use = list(get_default_maps())

        # 3. Remove disabled maps
        if disable:
            maps_to_use = [m for m in maps_to_use if m not in disable]

        # 4. Add positional maps
        if maps:
            maps_to_use.extend(maps)

        # 5. Add enabled maps
        if enable:
            maps_to_use.extend(enable)

    # 6. Apply maps in order
    for m in maps_to_use:
        if isinstance(m, type) and is_dataclass(m):
            m = m()

        if is_dataclass(m):
            pattern = m.get_syntax()
            d = m.as_map()

        elif hasattr(m, "as_dict"):
            pattern = Syntax.angles
            d = m.as_dict()

        elif isinstance(m, dict):
            pattern = runtime.get("syntax")
            if not pattern:
                continue
            d = m

        else:
            continue

        def repl(match):
            k = match.group(1)
            return str(d.get(k, match.group(0)))

        text = re.sub(pattern, repl, text)

    # 7. Runtime kwargs always apply last
    if runtime:
        pattern = Syntax.braces
        d = runtime

        def repl(match):
            k = match.group(1)
            return str(d.get(k, match.group(0)))

        text = re.sub(pattern, repl, text)

    return text

