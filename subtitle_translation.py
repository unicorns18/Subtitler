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
from typing import Any, Dict
import os
import srt

from subtitles import FileReader

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

        print(data)

        if data["type"] == "json":
            # TODO: Detect language using langdetect

            print("translate() json")
            # TODO: do processing (JSON)
        elif data["type"] == "srt":
            print("translate() srt")
            # TODO: do processing (SRT)

        return self.srt_file
    
    def _translate_sub(self, sub_content: str, target_language: str) -> str:
        """
        Translates a single subtitle to the target language.

        Args:
            sub_content (str): The content of the subtitle to be translated.
            target_language (str): The language to translate the subtitle to.

        Raises:
            NotImplementedError: If the method is not implemented.
            ValueError: If the target language is not supported.
            LangDetectException: If the language of the subtitle could not be detected.

        Returns:
            str: The translated subtitle.
        """
        supported_languages = [
            'af', 'am', 'ar', 'as', 'az', 'ba', 'be', 'bg', 'bn', 'bo', 'br', 'bs', 'ca', 'cs',
            'es', 'et', 'eu', 'fa', 'fi', 'fo', 'fr', 'gl', 'gu', 'ha', 'haw', 'he', 'hi', 'hr',
            'it', 'ja', 'jw', 'ka', 'kk', 'km', 'kn', 'ko', 'la', 'lb', 'ln', 'lo', 'lt', 'lv',
            'mi', 'mk', 'ml', 'mn', 'da', 'de', 'el', 'en', 'hu', 'hy', 'id', 'is', 'ro', 'ru',
            'mr', 'ms', 'mt', 'my', 'ne', 'nl', 'nn', 'no', 'oc', 'pa', 'pl', 'ps', 'lt', 'lv',
            'sl', 'sn', 'so', 'sq', 'sr', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'sd', 'si',
            'tk', 'tl', 'tr', 'tt', 'uk', 'ur', 'uz', 'vi', 'yi', 'yo', 'zh',
            'pt', 'sk', 'mg', 'sa', 'mg', 'ht', 'cy',
        ]
        if target_language not in supported_languages:
            raise ValueError("The target language is not supported.")

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

os.system("cls")
st = SubtitleTranslation("ja", "en", "test.srt")
translation = st.translate()
print(translation)