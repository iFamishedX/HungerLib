import re
from dataclasses import dataclass, fields, is_dataclass


class Syntax:
    BRACES   = r"\{([^{}]+)\}"      # {key}
    DOLLARS  = r"\$\{([^{}]+)\}"    # ${key}
    ANGLES   = r"<([^<>]+)>"        # <key>
    PERCENTS = r"%([^%]+)%"         # %key%


@dataclass
class DataMap:
    __syntax__: str = Syntax.BRACES

    def as_map(self) -> dict:
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if f.init and f.name != "__syntax__"
        }

    @classmethod
    def syntax(cls) -> str:
        return getattr(cls, "__syntax__", Syntax.BRACES)


def mapit(text: str, *maps, **runtime) -> str:
    for m in maps:
        # auto-instantiate dataclass classes
        if isinstance(m, type) and is_dataclass(m):
            m = m()

        # dataclass instance to dict
        if is_dataclass(m):
            pattern = m.syntax()
            dmap = m.as_map()

        # colormap-like objects to dict
        elif hasattr(m, "as_dict"):
            pattern = Syntax.ANGLES
            dmap = m.as_dict()

        # raw dict
        elif isinstance(m, dict):
            pattern = runtime.get("syntax", None)
            if not pattern:
                continue
            dmap = m

        else:
            continue

        # apply this map's syntax only
        def repl(match):
            key = match.group(1)
            return str(dmap.get(key, match.group(0)))
        text = re.sub(pattern, repl, text)

    return text
