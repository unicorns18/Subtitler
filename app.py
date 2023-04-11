"""
This module provides a class for extracting audio from video files using the ffmpeg library.

Classes:
    AudioExtraction: A class for extracting audio from video files.

Exceptions:
    AudioExtractionError:
        An exception raised if an error occurs while extracting audio from a video file.
"""

import subprocess
import os
from exceptions import AudioExtractionError

class AudioExtraction():
    """
    Extracts audio from a video file.

    Attributes:
        input_file (str): The path to the video file.
        audio_file_name (str): The path to the audio file.
    """

    input_file = None
    audio_file_name = None

    def __init__(self, input_file, audio_file_name=None):
        self.input_file = input_file
        if audio_file_name is None:
            self.audio_file_name = os.path.curdir + "/audio/" + \
                       os.path.basename(input_file).split(".")[0] + \
                       ".wav"

    def extract_audio(self):
        """
        Extracts audio from the input video file and saves it to a file.

        Raises:
            AudioExtractionError: If an error occurs while extracting the audio.
        """
        command = (f"ffmpeg -hide_banner -loglevel warning -i {self.input_file} "
                   f"-b:a 192k -ac 1 -ar 16000 -vn {self.audio_file_name}")
        try:
            subprocess.call(command, shell=True)
            print(f"Extracted audio to audio/{self.audio_file_name.split('/')[-1]}")
        except subprocess.CalledProcessError as error:
            raise AudioExtractionError('Error extracting audio. '
                           'Please check the video file and try again.') from error

ae = AudioExtraction("E:\\S01E01.mkv")
ae.extract_audio()
