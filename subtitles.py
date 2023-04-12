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
import chardet

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

    def __init__(self, srt_file: List[str]) -> None:
        """
        Initializes an instance of the SRTProcessing class.

        Args:
            srt_file (List[str]): A list of strings containing the SRT file data.
        """
        self.srt_file = srt_file
    def detect_encoding(self) -> str:
        """
        Detects the encoding of the SRT file.

        Raises:
            UnicodeDecodeError: If the SRT file is not encoded in any of the supported encodings.
            IOError: If the SRT file could not be read.
        
        Returns:
            str: The encoding of the SRT file.
        """
        try:
            with open(self.srt_file, 'rb') as file:
                raw_data = file.read()
                encoding = chardet.detect(raw_data)['encoding']
                if encoding is None:
                    raise UnicodeDecodeError(
                        f"Unsupported encoding detected in file. {self.srt_file}"
                        )
                return encoding
        except UnicodeDecodeError as err:
            raise UnicodeDecodeError(
                f"Unsupported encoding detected in file. {self.srt_file}"
                ) from err
        except IOError as err:
            raise IOError("Could not read the SRT file.") from err
    def translate(self, source_language: str, target_language: str) -> List[str]:
        """
        Translates the captions in the SRT file to the target language.

        Args:
            source_language (str): The language of the captions in the SRT file.
            target_language (str): The language to translate the captions to.

        Returns:
            List[str]: A list of strings containing the translated SRT file data.
        """
        try:
            with open(self.srt_file, 'r', encoding=self.detect_encoding()) as file:
                srt_data = file.read()
        except UnicodeDecodeError as unicodedecodeerror:
            raise UnicodeDecodeError(
                f"Unsupported encoding detected in file. {self.srt_file}"
                ) from unicodedecodeerror
        except IOError as err:
            raise IOError("Could not read the SRT file.") from err
        try:
            subs = list(srt.parse(srt_data))
        except srt.SRTParseError as srtparseerr:
            raise SRTException("The SRT file is invalid or malformed.") from srtparseerr
        translated_subs = []

        for sub in subs:
            try:
                source_lang = detect(sub.content)
                if source_lang != source_language:
                    continue
            except Exception as translationerror:
                raise TranslationError(
                    "An error occurred while translating the subtitles."
                    ) from translationerror
            try:
                translated_sub = self._translate_sub(sub.content, target_language)
            except Exception as error2:
                raise TranslationError(
                    "An error occurred while translating the subtitles."
                    ) from error2
            translated_subs.append(
                srt.Subtitle(
                    index=sub.index,
                    start=sub.start,
                    end=sub.end,
                    content=translated_sub
                )
            )

        return srt.compose(translated_subs)
    def _translate_sub(self, sub_content: str, target_language: str) -> str:
        """
        Translates a single subtitle to the target language.

        Args:
            sub_content (str): The content of the subtitle to be translated.
            target_language (str): The language to translate the subtitle to.

        Returns:
            str: The translated subtitle.
        """
        # TODO: Implement translation logic
        target_language = target_language.lower()
        return sub_content

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


os.system("cls")
# st = SubtitleTranslation("ja", "en", "other\\transcription_replicate.json")
# translation = st.translate()
