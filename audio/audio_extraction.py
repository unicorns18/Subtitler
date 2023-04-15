"""
The audio_extraction module provides a simple interface for extracting audio from,
video files using ffmpeg.

Classes:
    - AudioExtraction: A class for extracting audio from video files.

Exceptions:
    AudioExtractionError: If the audio track can't be extracted from the input video file.
    FileNotFoundError: If the input video file or output directory doesn't exist.
    ValueError: If the language choice is invalid.

Fields:
    - input_video_file_path: Path of input video file.
    - output_audio_file_path: Path of output audio file.

Methods:
    - extract_audio: Extracts audio from video.

Usage:
To extract audio from a video file,
create an instance of AudioExtraction and call the extract_audio method:
```
from audio_extraction import AudioExtraction, AudioExtractionError

try:
    audio_extractor = AudioExtraction('/path/to/video.mp4', '/path/to/audio.wav')
    audio_extractor.extract_audio()
except AudioExtractionError as e:
    print('An error occurred while extracting audio:', e)
```
"""
import subprocess
import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # pylint: disable=import-error, wrong-import-position
from exceptions.exceptions import AudioExtractionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioExtraction:
    """
    Audio Extraction from video.

    Attributes
    ----------
    input_video_file_path: str
        Path of input video file.
    output_audio_file_path: str
        Path of output audio file.

    Methods
    -------
    get_language_choice(language_track_mapping: dict) -> str
        Get the language choice.
    extract_audio() -> None
        Extracts audio from video.

    Raises
    ------
    AudioExtractionError
        If the audio track can't be extracted from the input video file.
    FileNotFoundError
        If the input video file or output directory doesn't exist.
    ValueError
        If the language choice is invalid.
    """

    def __init__(self, input_video_file_path: str, output_audio_file_path: str) -> None:
        self.input_video_file_path = input_video_file_path
        self.output_audio_file_path = output_audio_file_path

    def get_language_choice(self, language_track_mapping: Dict[str, str]) -> str:
        """
        Get the language choice.

        Parameters
        ----------
        language_track_mapping: dict
            Language track mapping.

        Returns
        -------
        str
            Language choice.
        """
        # Display available languages
        logging.info("Available languages: ")
        for language in language_track_mapping:
            logging.info("%s: %s", language, language_track_mapping[language])

        # Prompt user for language choice
        language_choice = input(
            "Please choose a language (Example: eng or 1): ")

        # If the user's choice is a digit, convert it to an integer and verify it's valid
        if language_choice.isdigit():
            language_choice = int(language_choice)
            if language_choice < 1 or language_choice > len(language_track_mapping):
                raise ValueError(f"Invalid language choice: {language_choice}")
            # Convert the integer back to the corresponding language choice
            language_choice = list(language_track_mapping.keys())[
                language_choice - 1]
        else:
            # Verify that the user's choice is valid
            if language_choice not in language_track_mapping:
                raise ValueError(f"Invalid language choice: {language_choice}")
        # Return the language choice
        return language_choice

    def extract_audio(self) -> None:
        """
        Extracts the audio track from the input video file.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        AudioExtractionError
            If the audio track can't be extracted from the input video file.
        FileNotFoundError
            If the input video file or output directory doesn't exist.
        ValueError
            If the language choice is invalid.
        """
        # Initialize variables
        language_choice: Optional[str] = None
        language_track_mapping: Dict[str, str] = {}
        input_video_file = Path(self.input_video_file_path)

        # Check if the input video file exists
        if not input_video_file.is_file():
            raise FileNotFoundError(
                f"Input video file not found: {input_video_file}")

        # Check if the output directory exists
        if not Path(self.output_audio_file_path).parent.is_dir():
            raise FileNotFoundError(
                f"Output directory not found: {self.output_audio_file_path.parent}")

        # Execute ffprobe command to extract audio tracks information
        try:
            command = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'a',
                '-show_entries', 'stream=index:stream_tags=language',
                '-of', 'default=nokey=1:noprint_wrappers=1',
                self.input_video_file_path
            ]
            audio_tracks_info: List[str] = []
        except subprocess.CalledProcessError as ex:
            raise AudioExtractionError(ex) from ex

        # Get the output of ffprobe command
        try:
            audio_tracks_info = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT).decode('utf-8').split('\n')
        except subprocess.CalledProcessError as subprocess_error:
            raise AudioExtractionError(
                subprocess_error.output.decode('utf-8')
            ) from subprocess_error
        except FileNotFoundError as file_not_found_error:
            raise AudioExtractionError(file_not_found_error) from file_not_found_error

        # Remove empty elements from the output list and remove the '\r' character from each element
        audio_tracks_info = [
            track for track in audio_tracks_info if track != '']
        # remove the \r character from each element
        formatted_audio_tracks_info = [el.strip() for el in audio_tracks_info]

        # Create a language to track number mapping dictionary
        language_track_mapping = {}
        for i in range(0, len(formatted_audio_tracks_info), 2):
            language = formatted_audio_tracks_info[i + 1]
            track_number = formatted_audio_tracks_info[i]
            language_track_mapping[language] = track_number

        # Validate language choice
        if language_choice is None:
            language_choice = self.get_language_choice(language_track_mapping)
        if language_choice not in language_track_mapping:
            raise ValueError(f"Invalid language choice: {language_choice}")
        track_number = language_track_mapping[language_choice]

        print("You have selected track number", track_number)

        # Sanitize command
        command = (
            f'ffmpeg -i {self.input_video_file_path} '
            f'-map 0:a:{track_number} '
            f'-c copy {self.output_audio_file_path}'
        )

        # Execute ffmpeg command to extract audio track from the input video file,
        # and save it to the output audio file
        try:
            result = subprocess.run(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
            if result.returncode != 0:
                raise AudioExtractionError(result.stderr.decode('utf-8'))
        except FileNotFoundError as file_not_found_error:
            raise AudioExtractionError(file_not_found_error) from file_not_found_error
        except subprocess.CalledProcessError as called_process_error:
            raise AudioExtractionError(
                called_process_error.stderr.decode('utf-8')
            ) from called_process_error

        logging.info("Audio track: %s, audio_track_lang: %s extracted successfully.",
                     track_number, language_choice)

try:
    audio_extraction = AudioExtraction(
        input_video_file_path="E:\\S01E01.mkv",
        output_audio_file_path="E:\\S01E01_audio.wav"
    )
    audio_extraction.extract_audio()
except AudioExtractionError as error:
    logging.error(error)
except FileNotFoundError as error:
    logging.error(error)
except ValueError as error:
    logging.error(error)
