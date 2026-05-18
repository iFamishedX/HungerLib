import re
from dataclasses import dataclass, fields, is_dataclass

# global maps
_GLOBAL_MAPS = []

def setGlobalMaps(*maps: dict | "DataMap") -> None:
    '''Creates a list of global maps from the input.'''
    global _GLOBAL_MAPS
    _GLOBAL_MAPS = list(maps)

def getGlobalMaps() -> list:
    '''Returns the list of global maps in a list.'''
    return _GLOBAL_MAPS


# syntax patterns
class Syntax:
    '''Pre-built syntax object'''
    braces   = r"\{([^{}]+)\}"       # {example}
    dollars  = r"\$\{([^{}]+)\}"     # ${example}
    angles   = r"<([^<>]+)>"         # <example>
    percents = r"%([^%]+)%"          # %example%


# base datamap
@dataclass
class DataMap:
    '''Core datamap class. Contains logic used to make datamaps'''
    __syntax__: str = Syntax.braces
    __mode__ = None

    def as_map(self):
        result = {}

        for f in fields(self):
            if not f.init or f.name in ("__syntax__", "__mode__"):
                continue

            val = getattr(self, f.name)

            # dynamic mode
            if self.__mode__ == "dynamic":
                providers = getattr(self, "providers", None)

                # explicit provider dict only
                if isinstance(providers, dict) and f.name in providers:
                    val = providers[f.name]

                # callables are executed
                if callable(val):
                    val = val()

            result[f.name] = val

        return result

    @classmethod
    def get_syntax(cls):
        return getattr(cls, "__syntax__", Syntax.braces)


# decorator
def datamap(
    _cls = None,
    *,
    syntax: str = Syntax.braces,
    mode: bool | None = None,
):
    '''@datamap decorator with optional values'''
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
    '''Internal function to use mapit multiple times to map newly uncovered values'''
    current = text
    for _ in range(max_depth):
        result = mapit(
            current,
            extra_maps=extra_maps,
            override_maps=override_maps,
            recursive=False,
            **ctx
        )
        if result == current:
            return result
        current = result
    return current


# mapit function
def mapit(
    text: str,
    extra_maps: list | None = None,
    override_maps: list | None = None,
    recursive: bool = True,
    **ctx,
):
    '''
    HungerLib's Core Templating Engine
    Mapit is a powerful utility used to recursively map placeholders and keys to new values.
    Paramaters:
    - text: the string to map
    - extra_maps: maps to temporarily append to the list of global maps
    - override_maps: mapit will ignore global maps and extra_maps
    - recursive: whether mapit will map nested placeholders and keys
    - **ctx: use value=value to add in extra mappable paramaters
    '''
    if override_maps is not None:
        maps = list(override_maps)
    else:
        maps = list(getGlobalMaps())
        if extra_maps:
            maps.extend(extra_maps)

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

    if ctx:
        pattern = Syntax.braces
        d = ctx

        def repl(match):
            k = match.group(1)
            return str(d.get(k, match.group(0)))

        text = re.sub(pattern, repl, text)

    if recursive:
        return _recursive_map(text, extra_maps, override_maps, ctx)

    return text
