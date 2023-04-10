import subprocess, json, wavfile, os

pathtovideo = "E:\\S01E01.mkv"
pathtoffmpeg = "C:\\ffmpeg-2023-04-06-git-b564ad8eac-full_build\\bin\\"
pathtoffprobe = "C:\\ffmpeg-2023-04-06-git-b564ad8eac-full_build\\bin\\"

class AudioExtraction():
    input_file = None
    audio_file_name = None

    def __init__(self, input_file, audio_file_name=None):
        self.input_file = input_file
        if audio_file_name is None:
            self.audio_file_name = os.path.curdir + "/audio/" + os.path.basename(input_file).split(".")[0] + ".wav"

    def extractAudio(self):
        command = pathtoffmpeg+"ffmpeg -hide_banner -loglevel warning -i {} -b:a 192k -ac 1 -ar 16000 -vn {}".format(self.input_file, self.audio_file_name)

        try:
            ret = subprocess.call(command, shell=True)
            print("Extracted audio to audio/{}".format(self.audio_file_name.split("/")[-1]))
        except Exception as e:
            print("Error: ", str(e))
            exit(1)

ae = AudioExtraction(pathtovideo)
ae.extractAudio()