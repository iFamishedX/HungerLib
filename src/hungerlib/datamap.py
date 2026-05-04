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
        cls = type(cls.__name__, (DataMap,), dict(cls.__dict__))
        return dataclass(cls)
    return wrap if _cls is None else wrap(_cls)

datamap.braces = datamap(syntax=Syntax.braces)
datamap.angles = datamap(syntax=Syntax.angles)
datamap.dollars = datamap(syntax=Syntax.dollars)
datamap.percents = datamap(syntax=Syntax.percents)

def mapit(text: str, *maps, **runtime):
    maps = (*get_default_maps(), *maps)
    for m in maps:
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
    if runtime:
        pattern = Syntax.braces
        d = runtime
        def repl(match):
            k = match.group(1)
            return str(d.get(k, match.group(0)))
        text = re.sub(pattern, repl, text)
    return text
