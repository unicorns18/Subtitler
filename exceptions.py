"""This module defines custom exception classes for handling errors in a Python application.

The module defines two exception classes:

- NoDotEnvFile: An exception that is raised when a `.env` file is not found.
- UnknownException: An exception that is raised when an unknown or unexpected error occurs.

These exceptions can be used to provide more detailed error messages to users of the application.
"""


class NoDotEnvFile(Exception):
    """
    Exception raised when no `.env` file is found.

    Usage:
        This exception can be raised when a program requires a `.env` file but none is found. 
        The `message` parameter should be used to describe the specific details of the error.

        For example:
        `raise NoDotEnvFile("Could not find a .env file in the current directory.")`
    """

class UnknownException(Exception):
    """
    An exception class for handling unknown or unexpected errors.

    Usage:
        This exception can be raised when an unknown or unexpected error occurs. The `message`
        parameter should be used to describe the specific details of the error. For example:
        `raise UnknownException("An unknown error occurred.")`
    """


class AudioExtractionError(Exception):
    """
    An exception class for handling errors that occur during audio extraction.

    Usage:
        This exception can be raised when an error occurs during audio extraction. The `message`
        parameter should be used to describe the specific details of the error. For example:
        `raise AudioExtractionError("Could not extract audio from the video file.")`
    """


class SRTException(Exception):
    """
    An exception class for handling errors that occur during SRT processing.

    Usage:
        This exception can be raised when an error occurs during SRT processing. The `message`
        parameter should be used to describe the specific details of the error. For example:
        `raise SRTException("Could not parse the SRT file.")`
    """

class TranslationError(Exception):
    """
    An exception class for handling errors that occur during translation.
    
    Usage:
        This exception can be raised when an error occurs during translation. The `message`
        parameter should be used to describe the specific details of the error. For example:
        `raise TranslationError("Could not translate the subtitles.")`
    """
    