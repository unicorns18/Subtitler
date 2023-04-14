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
    data (Dict[str, Any]): A dictionary containing the subtitle file data.

Usage:
    >>> from subtitles import FileReader
    >>> file = FileReader("path/to/subtitle.srt")
    >>> file.read()
    {'type': 'srt', 'data': [Subtitle(index=1, start=datetime.timedelta(seconds=10, microseconds=500000), end=datetime.timedelta(seconds=13), content="Look! It's a huge explosion!", proprietary='')]} # #pylint: disable=line-too-long
"""
from typing import Any, Dict, List, Union
from pathlib import Path
import os
import srt
from exceptions import UnknownException, FileReadError, SubtitleTypeNotRecognized, SRTParseError

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

    def read(self) -> Dict[str, Union[str, List[Any]]]:
        """
        Reads the subtitle file data and returns it in a dictionary format.

        Returns:
            data (Dict[str, Union[str, List[Any]]]): A dictionary containing the subtitle file data.

        Raises:
            UnknownException: If the file type is not recognized.
            FileNotFoundError: If the file could not be found.
            FileReadError: If the file could not be read.
            SRTParseError: If the SRT file could not be parsed.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"File could not be found: {self.path}")

        if self.path.suffix not in (".srt", ".json", ".jsonl"):
            raise SubtitleTypeNotRecognized(f"File type not recognized: {self.path.suffix}")

        if self.path.suffix == ".srt":
            if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
                with open(self.path, "r", encoding="utf-8") as file:
                    try:
                        return {
                            "type": "srt",
                            "data": list(srt.parse(file.read()))
                        }
                    except srt.SRTParseError as srt_parse_error:
                        raise SRTParseError(f"File could not be parsed: {self.path}") from srt_parse_error
            else:
                raise FileReadError(f"File could not be read: {self.path}")

        elif self.path.suffix == ".json" or self.path.suffix == ".jsonl":
            if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
                with open(self.path, "r", encoding="utf-8") as file:
                    return {
                        "type": "json",
                        "data": file.read()
                    }
            else:
                raise FileReadError(f"File could not be read: {self.path}")

        return {"type": "unknown", "data": None}
     
try:
    input_file = input("1 for JSON, 2 for SRT, 3 for none: ")
    if input_file == "1":
        fr = FileReader("other/whisper-1-new.json")
    elif input_file == "2":
        fr = FileReader("other/test_en.srt")
    elif input_file == "3":
        exit()
    else:
        raise ValueError("Invalid input")
    data = fr.read()
    print(data)
except (UnknownException, FileNotFoundError, FileReadError) as exception:
    print(exception)
    raise exception