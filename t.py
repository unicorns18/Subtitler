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
from typing import List, Union

import srt
from langdetect import DetectorFactory

from exceptions import UnknownException

DetectorFactory.seed = 0

class SRTProcessing:
    """
    Class for processing SRT subtitle files.

    Attributes:
        srt_file (str): The path to the SRT file to be processed.

    Raises:
        IOError: If the SRT file could not be read.
        SRTException: If the SRT file is invalid or malformed.
        TranslationError: If an error occurs during translation.

    Usage:
        srt_processor = SRTProcessing('/path/to/srt/file.srt')
        srt_processor.translate('en', 'es')
    """

    def __init__(self, srt_file):
        """
        Initializes an instance of the SRTProcessing class.

        Args:
            srt_file (List[str]): A list of strings containing the SRT file data.
        """
        self.srt_file = srt_file

    def translate(self, source_language: str, target_language: str) -> List[str]:
        """
        Translates the captions in the SRT file to the target language.

        Args:
            source_language (str): The language of the captions in the SRT file.
            target_language (str): The language to translate the captions to.

        Returns:
            List[str]: A list of strings containing the translated SRT file data.
        """
        # TODO: do processing (SRT)


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
            return {"type": "srt", "data": srt.parse(open(self.path, "r", encoding="utf-8").read())}
        if self.path.endswith(".json"):
            print("json")
            return {"type": "json", "data": open(self.path, "r", encoding="utf-8").read()}
        print("unknown")
        raise UnknownException("Unknown file type")


class SubtitleTranslation:
    """
    A class for translating subtitle files from one language to another.

    Attributes:
        source_language (str): The source language of the subtitles.
        target_language (str): The target language to which the subtitles should be translated.
        srt_file (str): The path to the subtitle file that should be translated.
    """

    def __init__(self, source_language, target_language, srt_file):
        self.source_language = source_language
        self.target_language = target_language
        self.srt_file = srt_file

    def translate(self):
        """
        Translates the captions in the subtitle file to the target language.

        Returns:
            The path to the translated subtitle file.

        Raises:
            TranslationError: If an error occurs while translating the subtitles.
        """
        file = FileReader(self.srt_file)
        data = file.read()

        if data["type"] == "json":
            # TODO: Detect language using langdetect

            print("translate() json")
            # TODO: do processing (JSON)
        elif data["type"] == "srt":
            print("translate() srt")
            # TODO: do processing (SRT)

        return self.srt_file

    def save(self, path):
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


os.system("cls")
st = SubtitleTranslation("ja", "en", "other\\transcription_replicate.json")
translation = st.translate()
