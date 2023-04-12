"""

"""
from typing import List
import errno
import srt
import chardet

from exceptions import SRTException, TranslationError

from subtitle_translation import SubtitleTranslation

try:
    from langdetect import detect
except ImportError as error:
    raise ImportError(
        "The `langdetect` module is required for this program to run. "
        "Please install it using `pip install langdetect`."
    ) from error

SUPPORTED_ENCODINGS = ['utf-8', 'UTF-8-SIG', 'ascii', 'iso-8859-1',
                       'utf-16', 'utf-16-le', 'utf-16-be', 'cp1252', 'cp850', 'cp437']


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
            FileNotFoundError: If the SRT file could not be found.
            IOError: If the SRT file could not be read.

        Returns:
            str: The encoding of the SRT file.
        """
        try:
            with open(self.srt_file, 'rb') as file:
                raw_data = file.read()
                encoding = chardet.detect(raw_data)['encoding']
                if encoding is None or encoding not in SUPPORTED_ENCODINGS:
                    raise UnicodeDecodeError(
                        encoding,
                        raw_data,
                        0,
                        0,
                        f"Unsupported encoding detected in file. {self.srt_file}",
                    )
                return encoding
        except (UnicodeDecodeError, FileNotFoundError):
            raise FileNotFoundError(
                errno.ENOENT, "The SRT file could not be found.") from None
        except IOError as err:
            raise IOError("Could not read the SRT file.") from err

    def translate(self, source_language: str, target_language: str) -> List[str]:
        """
        Translates the captions in the SRT file to the target language.

        Args:
            source_language (str): The language of the captions in the SRT file.
            target_language (str): The language to translate the captions to.

        Raises:
            IOError: If the SRT file could not be read.
            SRTException: If the SRT file is invalid or malformed.
            TranslationError: If an error occurs during translation.

        Returns:
            List[str]: A list of strings containing the translated SRT file data.
        """

        try:
            with open(self.srt_file, 'r', encoding=self.detect_encoding()) as file:
                srt_data = file.read()
        except IOError as err:
            raise IOError("Could not read the SRT file.") from err
        except UnicodeDecodeError as decode_error:
            raise UnicodeDecodeError(
                f"Unsupported encoding detected in file. {self.srt_file}"
            ) from decode_error

        try:
            subs = list(srt.parse(srt_data))
        except srt.SRTParseError as srtparseerr:
            raise SRTException(
                "The SRT file is invalid or malformed.") from srtparseerr

        translated_subs = []

        sub_trans = SubtitleTranslation(
            source_language=source_language,
            target_language=target_language,
            srt_file=self.srt_file
        )

        for sub in subs:
            try:
                source_lang = detect(sub.content)
                if source_lang != source_language:
                    continue
            except Exception as trans_err:
                raise TranslationError(
                    "An error occurred while translating the subtitles."
                ) from trans_err
            try:
                translated_sub = sub_trans.translate()
            except Exception as trans_err:
                raise TranslationError(
                    "An error occurred while translating the subtitles."
                ) from trans_err

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
            raise ValueError(
                f"The target language is not supported. {target_language}")
        
        return sub_content
