from deep_translator import MyMemoryTranslator
from os import system
import srt

class SRTProcessing():
    def __init__(self, srt_file):
        self.srt_file = srt_file

    def translate(self, source_language, target_language):
        # TODO: do processing (SRT)
        pass

class FileReader():
    def __init__(self, path):
        self.path = path
    
    def read(self):
        if self.path.endswith(".srt"):
            print("srt")
            return {"type": "srt", "data": srt.parse(open(self.path, "r", encoding="utf-8").read())}
        elif self.path.endswith(".json"):
            print("json")
            return {"type": "json", "data": open(self.path, "r", encoding="utf-8").read()}
        else:
            print("unknown")
            raise Exception("Unknown file type")
    
class SubtitleTranslation():
    def __init__(self, source_language, target_language, srt_file):
        self.source_language = source_language
        self.target_language = target_language
        self.srt_file = srt_file

    def translate(self):
        file = FileReader(self.srt_file)
        data = file.read()

        if data["type"] == "json":
            print("translate() json")
            # TODO: do processing (JSON)
        elif data["type"] == "srt":
            print("translate() srt")
            # TODO: do processing (SRT)

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(srt.compose(self.srt_file)) 

system("cls")
st = SubtitleTranslation("ja", "en", "other\\transcription_replicate.json")
translation = st.translate()
#print(translation)