"""
A module that reads a subtitle file and returns its data in a dictionary format.

Classes:
    FileReader: A class that reads a subtitle file and returns its data in a dictionary format.

Exceptions:
    UnknownException: If the file type is not recognized.

Usage:
    >>> from subtitles import FileReader
    >>> file = FileReader("path/to/subtitle.srt")
    >>> file.read()
    {'type': 'srt', 'data': <generator object parse at 0x000001F1F1B8F0A0>}
"""
from typing import Union
import srt
from exceptions import UnknownException

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
            return {
                "type": "srt",
                "data": list(srt.parse(open(self.path, "r", encoding="utf-8").read()))
            }
        if self.path.endswith(".json"):
            print("json")
            return {"type": "json", "data": open(self.path, "r", encoding="utf-8").read()}
        print("unknown")
        raise UnknownException("Unknown file type")
    
# fr = FileReader("test.srt")
# data = fr.read()
# print(data)
