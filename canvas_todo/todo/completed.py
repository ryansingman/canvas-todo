from enum import Enum


class Completed(Enum):
    """Enumerates completed states"""
    INCOMPLETE = 0
    UNKNOWN = 1
    COMPLETE = 2

    def __str__(self) -> str:
        """Converts enumerated obj to string

        Returns
        -------
        str
            string repr of enumeration
        """
        if self == self.INCOMPLETE:
            return " "
        elif self == self.UNKNOWN:
            return "?"
        else:
            return "X"