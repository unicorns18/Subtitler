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
import langdetect

from langdetect.lang_detect_exception import LangDetectException
from filereader import FileReader

from exceptions import TranslationError

from deep_translator import MyMemoryTranslator
from deep_translator.exceptions import NotValidLength, NotValidPayload, TranslationNotFound

SUPPORTED_ENCODINGS = ['utf-8', 'UTF-8-SIG', 'ascii', 'iso-8859-1',
                       'utf-16', 'utf-16-le', 'utf-16-be', 'cp1252', 'cp850', 'cp437']

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
            print("translate() json")
            # TODO: do processing (JSON)
        elif data["type"] == "srt":
            srt_contents = data["data"]
            content, translated_content = [], []
            for sub in srt_contents:
                content.append(sub.content)
            try:
                detected_language = langdetect.detect(" ".join(content))
            except LangDetectException as e:
                raise TranslationError("Could not detect language.") from e
            print(f"Detected language: {detected_language}")

            if detected_language != self.source_language:
                raise TranslationError("Detected language does not match source language.")
            
            for sub in content:
                try:
                    translated = MyMemoryTranslator(source=self.source_language, target=self.target_language).translate(sub)
                except (NotValidLength, NotValidPayload, TranslationNotFound) as e:
                    raise TranslationError("Could not translate subtitles.") from e
                print(f"Translated: {sub} -> {translated}")
                print("")
                translated_content.append(translated)

            for i, sub in enumerate(srt_contents):
                sub.content = translated_content[i]
            self.srt_file = srt_contents
            return srt_contents
        else:
            raise TranslationError("Could not read file.")
    
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
st = SubtitleTranslation("ja", "en", "test_ja.srt")
translation = st.translate()
st.save("test_translated_en.srt")
print(translation)
