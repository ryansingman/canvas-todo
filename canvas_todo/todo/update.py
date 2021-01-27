from enum import Enum


class Update(Enum):
    """Enumerates task update types
    """
    ADD = 0
    MARK_COMPLETE = 1