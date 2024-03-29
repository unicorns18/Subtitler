#pylint: disable=line-too-long,E1101
"""
The FileReader class reads a subtitle file and returns its data in a dictionary format. It can handle files with extensions .srt, .json, and .jsonl. The read() method reads the file data and returns it in a dictionary format with the type of the file and its data. It raises exceptions if the file type is not recognized, the file could not be found, or the file could not be read.

Classes:
    FileReader: A class that reads a subtitle file and returns its data in a dictionary format.

Exceptions:
    UnknownException: If the file type is not recognized.
    FileNotFoundError: If the file could not be found.
    FileReadError: If the file could not be read.

Methods:
    read(): Reads the subtitle file data and returns it in a dictionary format.

Returns:
    data (Dict[str, Union[str, List[Any]]]): A dictionary containing the subtitle file data.

Usage:
    >>> from subtitles import FileReader
    >>> file = FileReader("path/to/subtitle.srt")
    >>> file.read()
    {'type': SubtitleType.SRT, 'data': [Subtitle(index=1, start=datetime.timedelta(seconds=10, microseconds=500000), end=datetime.timedelta(seconds=13), content="Look! It's a huge explosion!", proprietary='')]} # #pylint: disable=line-too-long
"""
from typing import Any, Dict, List, Union
from pathlib import Path
import os
import sys
import srt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #pylint: disable=import-error, wrong-import-position
from exceptions.exceptions import FileReadError, SubtitleTypeNotRecognized, SRTParseError
from enums.subtitletype import SubtitleType

class FileReader:
    """
    A class that reads a subtitle file and returns its data in a dictionary format.

    Attributes:
        path (Union[str, bytes, Path]): The path to the subtitle file.

    Methods:
        read(): Reads the subtitle file data and returns it in a dictionary format.

    Returns:
        data (Dict[str, Union[str, List[Any]]]): A dictionary containing the subtitle file data.

    Raises:
        UnknownException: If the file type is not recognized.
        FileNotFoundError: If the file could not be found.
        FileReadError: If the file could not be read.
    """

    def __init__(self, path: Union[str, bytes, Path]) -> None:
        self.path = Path(path)

    def read(self) -> Dict[str, Union[SubtitleType, List[Any]]]:
        """
        Reads the subtitle file data and returns it in a dictionary format.

        Returns:
            data (Dict[str, Union[SubtitleType, List[Any]]]): A dictionary containing the subtitle file data.

        Raises:
            SubtitleTypeNotRecognized: If the file type is not recognized.
            FileNotFoundError: If the file could not be found.
            FileReadError: If the file could not be read.
            SRTParseError: If the file is not a valid SRT file.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"File could not be found: {self.path.resolve()}")

        if self.path.suffix not in (".srt", ".json", ".jsonl"):
            raise SubtitleTypeNotRecognized(f"File type not recognized: {self.path.suffix}")

        if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
            if self.path.suffix == ".srt":
                if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
                    with open(self.path, "r", encoding="utf-8") as file:
                        try:
                            return {
                                "type": SubtitleType.SRT.name,
                                "data": list(srt.parse(file.read()))
                            }
                        except srt.SRTParseError as srt_parse_error:
                            raise SRTParseError(f"File could not be parsed: {self.path}") from srt_parse_error

            elif self.path.suffix == ".json" or self.path.suffix == ".jsonl":
                if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
                    with open(self.path, "r", encoding="utf-8") as file:
                        return {
                            "type": SubtitleType.JSON.name if self.path.suffix == ".json" else SubtitleType.JSONL.name,
                            "data": file.read()
                        }
                    
        raise FileReadError(f"File could not be read: {self.path}")
     
# try:
#     input_file = input("1 for JSON, 2 for SRT, 3 for none: ")
#     if input_file == "1":
#         fr = FileReader("../files/whisper-1-new.json")
#     elif input_file == "2":
#         fr = FileReader("test_en.srt")
#     elif input_file == "3":
#         exit()
#     else:
#         raise ValueError("Invalid input")
#     data = fr.read()
#     print(data)
# except (UnknownException, FileNotFoundError, FileReadError) as exception:
#     print(exception)
#     raise exception
