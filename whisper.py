# import openai
# audio_file= open("E:\\Subtitler\\S01E01.mp3", "rb")
# a = openai.Audio.transcribe('whisper-1', audio_file, api_key="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")
# print(a.text)

from lhotse import CutSet, RecordingSet, align_with_torchaudio, annotate_with_whisper
from tqdm import tqdm
import ffmpeg, subprocess

def convert_to_mono(input_file, output_file):
    subprocess.call(["ffmpeg", "-y", "-i", input_file, "-ac", "1", output_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

convert_to_mono("E:\\Subtitler\\S01E01.mp3", "E:\\Subtitler\\S01E01_mono.mp3")
exit(0)
recordings = RecordingSet.from_dir("E:\\Subtitler\\", pattern="*.mp3")
recordings

cuts = annotate_with_whisper(recordings)
cuts

cuts_aligned = align_with_torchaudio(cuts)

with CutSet.open_writer("whisper-1.jsonl.gz") as writer:
    for cut in tqdm(cuts_aligned, desc="Writing cuts"):
        writer.write(cut)