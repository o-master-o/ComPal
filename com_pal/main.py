import os
import time

import speech_recognition
import whisper

from com_pal.hearing import SpeechRecognitionHearing
from com_pal.parsers import TxtParser
from com_pal.speech_recognizers import OpenaiWhisper
from com_pal.variables import CONFIG_DIR_PATH
from com_pal.voices import GoogleVoice

source = speech_recognition.Microphone()
recognizer = speech_recognition.Recognizer()
# model = GPT4All(GTP_MODEL_PATH, allow_download=False)


class PalAI:

    def __init__(self, name, voice, hearing, speech_recogniser, txt_parser):
        self.name = name
        self.voice = voice
        self.hearing = hearing
        self.speech_recogniser = speech_recogniser
        self.txt_parser = txt_parser
        self.user_name = None
        self._should_run = True

    def run(self):
        self._introduce_each_other()
        while self._should_run:
            self._assist_user()
        self.respond(f"Goodbye {self.user_name}. It was pleasure to serve you")

    def _introduce_each_other(self):
        self.respond(f"Hello, My name is {self.name}. I am your personal assistant")
        self.user_name = self._get_user_name()
        self.respond(f"Nice to meet you {self.user_name}. How can I help you")

    def _assist_user(self):
        output = self.listen_user()
        if not output:
            return
        if self._farewell_in(output):
            self._should_run = False
            return

        if self.address_assistant(output):
            self.respond(f'Yes {self.user_name}, right away')
            command = self.listen_user()
            self.perform_command(command)
            self.respond(f'Command is done')

        time.sleep(1)

    def _farewell_in(self, output):
        return f'goodbye, {self.name.lower()}' in output or f'goodbye {self.name.lower()}' in output

    def address_assistant(self, output):
        return self.name.lower() in output

    def respond(self, text):
        self.voice.say(text)

    def listen_user(self):
        tmp_wav_file_path = f"{CONFIG_DIR_PATH}/command.wav"
        with source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            with open("command.wav", "wb") as f:
                f.write(audio.get_wav_data())
        except speech_recognition.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except speech_recognition.RequestError:
            print("Unable to access the Google Speech Recognition API.")
            return None
        # self.hearing.listen(output_file_path=tmp_wav_file_path)
        return self.speech_recogniser.transcript("command.wav")

    def perform_command(self, command):
        if command:
            print("Command: ", command)
            self.respond(f'Executing  {command}')

    def _get_user_name(self):
        self.respond('May I ask your name?')
        output = self.listen_user()
        name = self.txt_parser.next_word_after_phrase(output, phrase="is ")
        while name is None:
            self.respond("I'm sorry. I did not understand you, Could you repeat your name?")
            name = self.txt_parser.next_word_after_phrase(self.listen_user(), phrase="my name is ")
        print(f'fetched name {name}')
        return name


if __name__ == "__main__":
    PalAI(
        name="Anna",
        voice=GoogleVoice('en'),
        hearing=SpeechRecognitionHearing(),
        speech_recogniser=OpenaiWhisper('/home/yoda/.config/com_pal/tiny.pt'),
        txt_parser=TxtParser
    ).run()

