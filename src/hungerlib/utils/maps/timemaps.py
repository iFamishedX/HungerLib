from datetime import datetime
from zoneinfo import ZoneInfo
from hungerlib.datamap import datamap, datamap_api


@datamap(syntax=datamap_api.percents, mode='dynamic')
class TimeMap:
    # default timezone
    _default_tz = ZoneInfo('UTC')

    # dynamic fields
    hh: str = None
    mm: str = None
    ss: str = None
    ms: str = None

    YYYY: str = None
    MM: str = None
    DD: str = None
    weekday: str = None

    def __new__(cls, tz: str | None = None):
        if tz is None:
            obj = super().__new__(cls)
            obj.TZ = cls._default_tz
            return obj

        obj = super().__new__(cls)
        obj.TZ = ZoneInfo(tz)
        return obj

    @property
    def providers(self):
        return {
            'hh':      lambda: f'{datetime.now(self.TZ).hour:02d}',
            'mm':      lambda: f'{datetime.now(self.TZ).minute:02d}',
            'ss':      lambda: f'{datetime.now(self.TZ).second:02d}',
            'ms':      lambda: f'{int(datetime.now(self.TZ).microsecond / 1000):03d}',

            'YYYY':    lambda: str(datetime.now(self.TZ).year),
            'MM':      lambda: f'{datetime.now(self.TZ).month:02d}',
            'DD':      lambda: f'{datetime.now(self.TZ).day:02d}',

            'weekday': lambda: datetime.now(self.TZ).strftime('%A'),
        }

# proxy map
TIME_MAP = TimeMap