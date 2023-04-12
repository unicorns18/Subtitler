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
import os
from typing import Union, List, Dict, Any

try:
    import srt
except ImportError as error:
    raise ImportError(
        "The `srt` module is required for this program to run. "
        "Please install it using `pip install srt`."
    ) from error

try:
    from langdetect import DetectorFactory, detect
except ImportError as error:
    raise ImportError(
        "The `langdetect` module is required for this program to run. " 
        "Please install it using `pip install langdetect`."
    ) from error

from exceptions import UnknownException, SRTException, TranslationError

DetectorFactory.seed = 0

SUPPORTED_ENCODINGS = ['utf-8', 'UTF-8-SIG', 'ascii', 'iso-8859-1', 'utf-16', 'utf-16-le', 'utf-16-be', 'cp1252', 'cp850', 'cp437']

class FileReader:
    """
    A class that reads a subtitle file and returns its data in a dictionary format.

    Attributes:
        path (str): The path to the subtitle file.

    Methods:
        read(): Reads the subtitle file data and returns it in a dictionary format.

    Raises:
        UnknownException: If the file type is not recognized.
    """

    def __init__(self, path: Union[str, bytes]) -> None:
        self.path = path

    def read(self):
        """
        Reads the subtitle file data and returns it in a dictionary format.

        Returns:
            dict: A dictionary containing the subtitle data.

        Raises:
            UnknownException: If the file type is not recognized.
        """
        if self.path.endswith(".srt"):
            print("srt")
            return {"type": "srt", "data": list(srt.parse(open(self.path, "r", encoding="utf-8").read()))}
        if self.path.endswith(".json"):
            print("json")
            return {"type": "json", "data": open(self.path, "r", encoding="utf-8").read()}
        print("unknown")
        raise UnknownException("Unknown file type")

class SubtitleTranslation:
    """
    A class for translating subtitle files from one language to another.

    Raises:
        TranslationError: If an error occurs while translating the subtitles.

    Attributes:
        source_language (str): The source language of the subtitles.
        target_language (str): The target language to which the subtitles should be translated.
        srt_file (str): The path to the subtitle file that should be translated.
    
    Methods:
        translate(): Translates the captions in the subtitle file to the target language.
        save(): Saves the translated subtitle file to the specified path.

    Usage:
        >>> from subtitle_translator import SubtitleTranslation
        >>> translator = SubtitleTranslation("en", "de", "path/to/subtitle.srt")
        >>> translator.translate()
        >>> translator.save("path/to/translated_subtitle.srt")
    """

    def __init__(self, source_language: str, target_language: str, srt_file: str) -> None:
        self.source_language = source_language
        self.target_language = target_language
        self.srt_file = srt_file

    def translate(self) -> str:
        """
        Translates the captions in the subtitle file to the target language.

        Returns:
            The path to the translated subtitle file.

        Raises:
            TranslationError: If an error occurs while translating the subtitles.
        """
        file = FileReader(self.srt_file)
        data: Dict[str, Any] = file.read()

        if data["type"] == "json":
            # TODO: Detect language using langdetect

            print("translate() json")
            # TODO: do processing (JSON)
        elif data["type"] == "srt":
            print("translate() srt")
            # TODO: do processing (SRT)

        return self.srt_file

    def save(self, path: str) -> None:
        """
        Saves the current SRT data to a file.

        Args:
            path (str): The path to the file to save.

        Raises:
            IOError: If the file could not be saved.
        """
        with open(path, "w", encoding="utf-8") as file:
            file.write(srt.compose(self.srt_file))
        if not os.path.isfile(path):
            raise IOError("Could not save file.")
        print(f"Saved file to {path}")
