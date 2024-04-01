import os
import sys
import time
import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import read as wav_read
from com_pal.variables import GTP_MODEL_PATH
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition
import whisper
from gpt4all import GPT4All
import pyttsx3
import pyautogui


def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    with BytesIO() as fp:
        tts.write_to_fp(fp)
        fp.seek(0)
        audio = AudioSegment.from_file(fp, format="mp3")
    play(audio)


# speak_text("hello, How are you. How can I help you")
engine = pyttsx3.init()
source = speech_recognition.Microphone()
recognizer = speech_recognition.Recognizer()
# model = GPT4All(GTP_MODEL_PATH, allow_download=False)
# base_model_path = os.path.expanduser('/home/yoda/.config/com_pal/base.pt')
base_model_path = os.path.expanduser('/home/yoda/.config/com_pal/tiny.pt')
base_model = whisper.load_model(base_model_path)


class PalAI:

    def __init__(self, name):
        self.name = name
        self.user_name = None
        self._should_run = True

    def run(self):
        self._introduce_each_other()
        while self._should_run:
            self._assist_user()
        self.respond("Goodbye.")

    def _build_trigger_phrase(self):
        return f"Hey {self.name}"

    def _introduce_each_other(self):
        self.respond(f"Hello, My name is {self.name}. I am your personal assistant")
        self.user_name = self._get_user_name()
        self.respond(f"Nice to meet you {self.user_name}. How can I help you")

    def _assist_user(self):
        output = self.listen_user()
        if not output:
            return
        print('====')
        print(output)
        print(f'goodbye, {self.name}.')
        print(f'goodbye, {self.name.lower()}' in output)
        print('====')
        if f'goodbye, {self.name.lower()}.' in output:
            print('exit')
            self._should_run = False
            return

        if self.address_assistant(output):
            self.respond(f'Yes {self.user_name}, right away')
            command = self.listen_user()
            self.perform_command(command)
            self.respond(f'Command is done')

        time.sleep(1)

    def address_assistant(self, output):
        return self.name.lower() in output

    def respond(self, text):
        engine.say(text)
        engine.runAndWait()

    def listen_user(self):
        with source:
            print("Listening for commands...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            with open("command.wav", "wb") as f:
                f.write(audio.get_wav_data())
            command = base_model.transcribe("command.wav", fp16=False)
            if command and command['text']:
                print("You said:", command['text'])
                return command['text'].lower()
            return None
        except speech_recognition.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except speech_recognition.RequestError:
            print("Unable to access the Google Speech Recognition API.")
            return None

    def perform_command(self, command):
        if command:
            print("Command: ", command)
            self.respond(f'Executing  {command}')

    def _get_user_name(self):
        self.respond('May I ask your name?')
        name = self._find_name_after_phrase(self.listen_user(), phrase="is ")
        while name is None:
            self.respond("I'm sorry. I did mot understand you, Could you repeat your name?")
            name = self._find_name_after_phrase(self.listen_user(), phrase="my name is ")
        print(f'fetched name {name}')
        return name

    def _find_name_after_phrase(self, text, phrase):
        start_index = text.find(phrase)

        if start_index != -1:
            next_word_start = start_index + len(phrase)
            text_after_phrase = text[next_word_start:]
            next_word_end = text_after_phrase.find(" ")
            if next_word_end == -1:
                next_word = text_after_phrase
            else:
                next_word = text_after_phrase[:next_word_end]
            return next_word
        return None


if __name__ == "__main__":
    PalAI("Dude").run()
