from config import TIMEZONE
from datetime import datetime
from pytz import timezone
from typing import Optional


def now_with_tz(tz: Optional[str]=None) -> datetime:
    """Return aware datetime instance with now date."""
    if tz is None:
        tz = TIMEZONE
    return datetime.now(tz=timezone(tz))
