# pylint: disable=logging-not-lazy, logging-fstring-interpolation,E1101
"""
This module provides a SubtitleTranslation class,
that can be used to translate subtitle files from,
one language to another using the langdetect library.

Classes:
    SubtitleTranslation: A class for translating subtitle files from one language to another.

Exceptions:
    TranslationError: If an error occurs while translating the subtitles.

Usage:
    >>> from subtitle_translator import SubtitleTranslation
    >>> translator = SubtitleTranslation("en", "de", "path/to/subtitle.srt")
    >>> translator.translate()
    >>> translator.save("path/to/translated_subtitle.srt")
"""
import logging
import os
import sys
from typing import Any, Dict, List
from contextlib import contextmanager
import srt
from srt import Subtitle
import langdetect
from deep_translator import MyMemoryTranslator
from deep_translator.exceptions import NotValidLength, NotValidPayload, TranslationNotFound
from langdetect.lang_detect_exception import LangDetectException
from enums.subtitletype import SubtitleType
from exceptions.exceptions import TranslationError
from file_handling.filereader import FileReader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # pylint: disable=import-error, wrong-import-position

SUPPORTED_ENCODINGS = ['utf-8', 'UTF-8-SIG', 'ascii', 'iso-8859-1',
                       'utf-16', 'utf-16-le', 'utf-16-be', 'cp1252', 'cp850', 'cp437']

logger = logging.getLogger(__name__)

# TODO: organize everything into functions
@contextmanager
def open_file(path: str, mode: str = "r", encoding: str = "utf-8"):
    """
    The objective of the open_file function is to provide a context manager that opens a file, yields it to the caller, and then closes it after the caller is done with it. This function is useful for ensuring that files are properly closed after use, even if an error occurs during file processing.

    Inputs:
        - path (str): a string representing the path to the file to be opened
        - mode (str): a string representing the mode in which the file should be opened (default is "r" for read mode)
        - encoding (str): a string representing the encoding of the file (default is "utf-8")

    Flow:
        1. The function takes in the path, mode, and encoding parameters.
        2. The function attempts to open the file using the given parameters.
        3. If the file is successfully opened, it is yielded to the caller.
        4. After the caller is done with the file, the file is closed using the 'finally' block.

    Outputs:
        - A file object that has been opened and yielded to the caller.

    Additional aspects:
        - The function uses the contextmanager decorator to create a context manager.
        - The function uses a try-finally block to ensure that the file is closed after use, even if an error occurs during file processing.
        - The function defaults to opening files in read mode with utf-8 encoding, but these parameters can be changed by the caller.
    """ # pylint: disable=line-too-long
    try:
        file = open(path, mode, encoding=encoding)
        yield file
    finally:
        file.close()

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

        if data["type"] == SubtitleType.JSON.name or data["type"] == SubtitleType.JSONL.name:
            print("translate() json")
            # TODO: do processing (JSON)
        elif data["type"] == SubtitleType.SRT.name:
            srt_contents: List[Subtitle] = data["data"]
            content, translated_content = [], []

            for sub in srt_contents:
                content.append(sub.content)

            try:
                detected_language = langdetect.detect(" ".join(content))
            except LangDetectException as langdetect_exception:
                logger.exception("Could not detect language.")
                raise TranslationError(
                    "Could not detect language.") from langdetect_exception
            logger.debug(f"Detected language: {detected_language}")

            if detected_language != self.source_language:
                logger.warning(
                    f"Detected language ({detected_language}) does not match source language ({self.source_language}).") # pylint: disable=line-too-long
                raise TranslationError(
                    f"Detected language ({detected_language}) does not match source language ({self.source_language}).") # pylint: disable=line-too-long

            for subtitle_content in content:
                try:
                    translated_subtitle = MyMemoryTranslator(
                        source=self.source_language,
                        target=self.target_language,
                    ).translate(subtitle_content)
                except (NotValidLength, NotValidPayload, TranslationNotFound) as translation_exception: # pylint: disable=line-too-long
                    logger.exception("Could not translate subtitle.")
                    raise TranslationError(
                        f"Could not translate subtitle: {subtitle_content}"
                    ) from translation_exception
                logger.debug(
                    f"Translated: {subtitle_content} -> {translated_subtitle}")
                logger.debug("")
                translated_content.append(translated_subtitle)

            for i, subtitle in enumerate(srt_contents):
                subtitle.content = translated_content[i]
            self.srt_file = srt_contents
            return str(self.srt_file)
        else:
            raise TranslationError(f"Could not read file: {self.srt_file}")

    def save(self, path: str) -> None:
        """
        Saves the current SRT data to a file.

        Args:
            path (str): The path to the file to save.

        Raises:
            IOError: If the file could not be saved.
        """
        try:
            with open_file(path, "w") as file:
                file.write(srt.compose(self.srt_file))
        except IOError as io_error:
            logger.exception("Could not save file.")
            raise IOError("Could not save file.") from io_error

os.system("cls")
st = SubtitleTranslation("ja", "en", "test_ja.srt")
TRANSLATION = st.translate()
st.save("test_en.srt")
print(TRANSLATION)
