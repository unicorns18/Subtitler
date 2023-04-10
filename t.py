import deepl, srt
from deep_translator import MyMemoryTranslator
from os import system

class FileReader():
    def __init__(self, path):
        self.path = path
    
    def read(self):
        if self.path.endswith(".srt"):
            print("srt")
            return {"type": "srt", "data": srt.parse(open(self.path, "r", encoding="utf-8").read())}
            #return srt.parse(open(self.path, "r", encoding="utf-8").read())
        elif self.path.endswith(".json"):
            print("json")
            return {"type": "json", "data": open(self.path, "r", encoding="utf-8").read()}
            #return self.path
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
        # for subtitle in self.srt_file:
        #     subtitle.content = MyMemoryTranslator(source=self.source_language, target=self.target_language).translate(subtitle.content)
        # return self.srt_file

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(srt.compose(self.srt_file)) 

system("cls")
st = SubtitleTranslation("ja", "en", "other\\transcription_replicate.json")
translation = st.translate()
#print(translation)