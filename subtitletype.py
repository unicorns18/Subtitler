#pylint: disable=line-too-long, invalid-name
"""
The SubtitleType class is an enumeration that defines the different types of subtitle files that can be used in a program. It provides a way to represent these types as constants with string values, making it easier to work with them in code. The class is designed to be used as a type hint for function arguments and return values, ensuring that only valid subtitle types are accepted or returned.

Methods:
    - __new__: This method is used internally by the Enum class to create new instances of the SubtitleType enumeration. It takes two arguments: the name of the constant and its value.
    - __str__: This method returns the string value of the constant, which is useful for displaying it in user interfaces or log messages.
    - __repr__: This method returns a string representation of the constant, which is useful for debugging and logging purposes.

Fields:
    - SRT: This constant represents the SRT subtitle type and has a string value of "srt".
    - JSON: This constant represents the JSON subtitle type and has a string value of "json".
    - JSONL: This constant represents the JSONL subtitle type and has a string value of "jsonl".
    - UNKNOWN: This constant represents an unknown subtitle type and has a string value of "unknown".
"""
from dataclasses import dataclass
from uniquevalueenum import UniqueValueEnum

@dataclass
class SubtitleType(UniqueValueEnum):
    """
    An enumeration that defines the different types of subtitle files that can be used in a program.
    
    Methods:
        __new__: This method is used internally by the Enum class to create new instances of the SubtitleType enumeration. It takes two arguments: the name of the constant and its value.
        __str__: This method returns the string value of the constant, which is useful for displaying it in user interfaces or log messages.
        __repr__: This method returns a string representation of the constant, which is useful for debugging and logging purposes.

    Fields:
        SRT: This constant represents the SRT subtitle type and has a string value of "srt".
        JSON: This constant represents the JSON subtitle type and has a string value of "json".
        JSONL: This constant represents the JSONL subtitle type and has a string value of "jsonl".
        UNKNOWN: This constant represents an unknown subtitle type and has a string value of "unknown".
    """
    SRT: str = "srt"
    JSON: str = "json"
    JSONL: str = "jsonl"
    UNKNOWN: str = "unknown"

    @classmethod
    def is_valid(cls, subtitle_type: str) -> bool:
        """
        This method checks if the given subtitle type is valid.

        Arguments:
            subtitle_type: The subtitle type to check.

        Returns:
            True if the subtitle type is valid, False otherwise.

        Usage:
            >>> SubtitleType.is_valid("srt")
            True
            >>> SubtitleType.is_valid("invalid")
            False
        """
        return subtitle_type in cls.__members__
    
    def __str__(self):
        return self.value
