from hungerlib import datamap, Syntax, mapit, set_default_maps

# ascii colormap
@datamap(syntax=Syntax.angles)
class ColorMap:
    black: str = "\033[30m"
    dark_blue: str = "\033[34m"
    dark_green: str = "\033[32m"
    dark_aqua: str = "\033[36m"
    dark_red: str = "\033[31m"
    dark_purple: str = "\033[35m"
    gold: str = "\033[33m"
    gray: str = "\033[37m"
    dark_gray: str = "\033[90m"
    blue: str = "\033[94m"
    green: str = "\033[92m"
    aqua: str = "\033[96m"
    red: str = "\033[91m"
    light_purple: str = "\033[95m"
    yellow: str = "\033[93m"
    white: str = "\033[97m"
    reset: str = "\033[0m"
    bold: str = "\033[1m"
    italic: str = "\033[3m"

    def as_dict(self):
        return {f"<{k}>": getattr(self, k) for k in self.__dataclass_fields__}


ASCII_COLOR_MAP = ColorMap()
