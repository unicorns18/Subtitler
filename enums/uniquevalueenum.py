#pylint: disable=line-too-long, invalid-name
"""
The UniqueValueEnum class is an enumeration that ensures that each constant has a unique value. It raises a ValueError if the value of the constant is not unique. This class can be used as a base class for other enumerations that require unique values for their constants.

Classes:
    UniqueValueEnum: An enumeration that ensures that each constant has a unique value.

Raises:
    ValueError: If the value of the constant is not unique.

Methods:
    __init__: This method is used internally by the Enum class to initialize new instances of the enumeration. It raises a ValueError if the value of the constant is not unique.

Usage:
    >>> from enum import Enum
    >>> class SubtitleType(UniqueValueEnum):
    ...     SRT = "srt"
    ...     JSON = "json"
    ...     JSONL = "jsonl"
    ...     UNKNOWN = "unknown"

Attributes:
    __init__: This method is used internally by the Enum class to initialize new instances of the enumeration. It raises a ValueError if the value of the constant is not unique.
"""
from enum import Enum

class UniqueValueEnum(Enum):
    """
    An enumeration that ensures that each constant has a unique value.

    Methods:
        __init__: This method is used internally by the Enum class to initialize new instances of the enumeration. It raises a ValueError if the value of the constant is not unique.

    Raises:
        ValueError: If the value of the constant is not unique.

    Usage:
        >>> from enum import Enum
        >>> class SubtitleType(UniqueValueEnum):
        ...     SRT = "srt"
        ...     JSON = "json"
        ...     JSONL = "jsonl"
        ...     UNKNOWN = "unknown"
    """
    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        if any(c1.value == value for c1 in cls):
            raise ValueError(f"duplicate value: {value!r}")
        return obj

    def __init__(self) -> None:
        cls = self.__class__
        if any(self.value == e.value for e in cls):
            raise ValueError(f'duplicate value: {self.value!r}')
        super().__init__()