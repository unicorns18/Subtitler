"""This module defines custom exception classes for handling errors in a Python application.

The module defines two exception classes:

- NoDotEnvFile: An exception that is raised when a `.env` file is not found.
- UnknownException: An exception that is raised when an unknown or unexpected error occurs.
- AudioExtractionError: An exception that is raised when an error occurs during audio extraction.
- SRTException: An exception that is raised when an error occurs during SRT processing.
- TranslationError: An exception that is raised when an error occurs during translation.
- FileReadError: An exception that is raised when an error occurs during file reading.
- SubtitleTypeNotRecognized: An exception that is raised when the subtitle type is not recognized.

These exceptions can be used to provide more detailed error messages to users of the application.
"""

class NoDotEnvFile(Exception):
    """
    Exception raised when no `.env` file is found.
    """

class UnknownException(Exception):
    """
    An exception class for handling unknown or unexpected errors.
    """

class AudioExtractionError(Exception):
    """
    An exception class for handling errors that occur during audio extraction.
    """

class SRTException(Exception):
    """
    An exception class for handling errors that occur during SRT processing.
    """

class TranslationError(Exception):
    """
    An exception class for handling errors that occur during translation.
    """

class FileReadError(Exception):
    """
    An exception class for handling errors that occur during file reading.
    """

class SubtitleTypeNotRecognized(Exception):
    """
    An exception class for handling errors that occur when the subtitle type is not recognized.
    """

class SRTParseError(Exception):
    """
    An exception class for handling errors that occur when the SRT file cannot be parsed.
    """

class InvalidEnumValueError(ValueError):
    """
    Exception raised when the value of enum is invalid.
    """
