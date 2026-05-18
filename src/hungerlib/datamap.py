import re
from dataclasses import dataclass, fields, is_dataclass

# global maps
_GLOBAL_MAPS = []

def setGlobalMaps(*maps):
    global _GLOBAL_MAPS
    _GLOBAL_MAPS = list(maps)

def getGlobalMaps():
    return _GLOBAL_MAPS


# syntax patterns
class Syntax:
    braces   = r"\{([^{}]+)\}"       # {example}
    dollars  = r"\$\{([^{}]+)\}"     # ${example}
    angles   = r"<([^<>]+)>"         # <example>
    percents = r"%([^%]+)%"          # %example%


# base datamap
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


# decorator
def datamap(_cls=None, *, syntax=Syntax.braces, mode=None):
    def wrap(cls):
        cls.__syntax__ = syntax
        cls.__mode__ = mode

        namespace = dict(cls.__dict__)
        namespace["__dict__"] = {}

        cls = type(cls.__name__, (DataMap,), namespace)
        return dataclass(frozen=False)(cls)

    return wrap if _cls is None else wrap(_cls)

# decorator shortcuts
datamap.braces = datamap(syntax=Syntax.braces)
datamap.angles = datamap(syntax=Syntax.angles)
datamap.dollars = datamap(syntax=Syntax.dollars)
datamap.percents = datamap(syntax=Syntax.percents)


# recursive wrapper
def _recursive_map(text, extra_maps, override_maps, ctx, max_depth=5):
    current = text

    for _ in range(max_depth):
        result = mapit(
            current,
            extra_maps=extra_maps,
            override_maps=override_maps,
            recursive=False,   # prevent infinite recursion
            **ctx
        )

        # stop if no change
        if result == current:
            return result

        current = result

    return current


# mapit function
def mapit(text: str, extra_maps=None, override_maps=None, recursive=True, **ctx):
    # determine maps to use
    if override_maps is not None:
        maps = list(override_maps)
    else:
        maps = list(getGlobalMaps())
        if extra_maps:
            maps.extend(extra_maps)

    # apply maps in order
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
            pattern = ctx.get("syntax")
            if not pattern:
                continue
            d = m

        else:
            continue

        def repl(match):
            k = match.group(1)
            return str(d.get(k, match.group(0)))

        text = re.sub(pattern, repl, text)

    # ctx vars always apply last (braces only)
    if ctx:
        pattern = Syntax.braces
        d = ctx

        def repl(match):
            k = match.group(1)
            return str(d.get(k, match.group(0)))

        text = re.sub(pattern, repl, text)

    # recursive expansion (default enabled)
    if recursive:
        return _recursive_map(text, extra_maps, override_maps, ctx)

    return text
