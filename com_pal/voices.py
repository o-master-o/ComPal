from abc import ABC, abstractmethod
from io import BytesIO

import pyttsx3
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


class Voice(ABC):

    @abstractmethod
    def say(self, text):
        pass


class GoogleVoice(Voice):

    def __init__(self, lang):
        self._lang = lang

    def say(self, text):
        tts = gTTS(text=text, lang=self._lang)
        with BytesIO() as fp:
            tts.write_to_fp(fp)
            fp.seek(0)
            audio = AudioSegment.from_file(fp, format="mp3")
        play(audio)


class Pyttsx3Voice(Voice):

    def __init__(self):
        self.engine = pyttsx3.init()

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
