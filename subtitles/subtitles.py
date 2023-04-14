"""
A module for translating subtitle files from one language to another.

The module defines the following classes:
- SRTProcessing: A class for processing SRT subtitle files.
- FileReader: A class that reads a subtitle file and returns its data in a dictionary format.
- SubtitleTranslation: A class for translating subtitle files from one language to another.

The module also defines the following exceptions:
- UnknownException: An exception that is raised when an unknown or unexpected error occurs.

These classes and exceptions can be used to translate subtitle files from one language to another.

Usage:
    from t import SubtitleTranslation

    subtitle_translation = SubtitleTranslation('en', 'es', '/path/to/srt/file.srt')
    subtitle_translation.translate()
"""
try:
    import srt
except (ModuleNotFoundError, ImportError) as error:
    raise ImportError(
        "The `srt` module is required for this program to run. "
        "Please install it using `pip install srt`."
    ) from error

try:
    from langdetect import DetectorFactory, detect
except (ModuleNotFoundError, ImportError) as error:
    raise ImportError(
        "The `langdetect` module is required for this program to run. " 
        "Please install it using `pip install langdetect`."
    ) from error

from exceptions.exceptions import UnknownException, SRTException, TranslationError

SUPPORTED_ENCODINGS = ['utf-8', 'UTF-8-SIG', 'ascii', 'iso-8859-1', 'utf-16', 'utf-16-le', 'utf-16-be', 'cp1252', 'cp850', 'cp437']