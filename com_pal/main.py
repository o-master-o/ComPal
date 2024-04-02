import time


from com_pal.hearing import SpeechRecognitionHearing
from com_pal.parsers import TxtParser
from com_pal.speech_recognizers import OpenaiWhisper
from com_pal.variables import CONFIG_DIR_PATH, GTP_MODEL_PATH, TINY_SPEECH_RECOGNITION_MODEL
from com_pal.voices import GoogleVoice
from gpt4all import GPT4All


class PalAI:

    def __init__(self, name, voice, hearing, speech_recogniser, txt_parser, assistant):
        self._name = name
        self._voice = voice
        self._hearing = hearing
        self._speech_recogniser = speech_recogniser
        self._txt_parser = txt_parser
        self._assistant = assistant
        self._user_name = None
        self._should_run = True

    def run(self):
        self._introduce_each_other()
        while self._should_run:
            self._assist_user()
        self.respond(f"Goodbye {self._user_name}. It was pleasure to serve you")

    def _introduce_each_other(self):
        self.respond(f"Hello, My name is {self._name}. I am your personal assistant")
        self._user_name = self._get_user_name()
        self.respond(f"Nice to meet you {self._user_name}. How can I help you")

    def _assist_user(self):
        output = self.listen_user()

        if not output:
            return

        if self._farewell_in(output):
            self._should_run = False
            return

        if self.address_assistant_in(output):
            self.respond(f'Yes {self._user_name}, right away')
            command = self.listen_user()
            self.perform_command(command)
            self.respond(f'Command is done')

        if self.question_in(output):
            self.respond("I'm listening. What is your question")
            output = self.listen_user()
            out = self._assistant.generate(output, max_tokens=200)
            print("Output: ", out)
            self.respond(out)

        time.sleep(1)

    def _farewell_in(self, output):
        return f'goodbye, {self._name.lower()}' in output or f'goodbye {self._name.lower()}' in output

    def address_assistant_in(self, output):
        return self._name.lower() in output

    def question_in(self, output):
        return 'question' in output

    def respond(self, text):
        self._voice.say(text)

    def listen_user(self):
        tmp_wav_file_path = f"{CONFIG_DIR_PATH}/command.wav"
        self._hearing.listen(output_file_path=tmp_wav_file_path)
        return self._speech_recogniser.transcript(tmp_wav_file_path)

    def perform_command(self, command):
        if command:
            print("Executing: ", command)
            self.respond(f'Executing  {command}')

    def _get_user_name(self):
        self.respond('May I ask your name?')
        output = self.listen_user()
        name = self._txt_parser.next_word_after_phrase(output, phrase="is ")
        while name is None:
            self.respond("I'm sorry. I did not understand you, Could you repeat your name?")
            name = self._txt_parser.next_word_after_phrase(self.listen_user(), phrase="my name is ")
        return name


if __name__ == "__main__":
    PalAI(
        name="Mary",
        voice=GoogleVoice('en'),
        hearing=SpeechRecognitionHearing(),
        speech_recogniser=OpenaiWhisper(TINY_SPEECH_RECOGNITION_MODEL),
        txt_parser=TxtParser,
        assistant=GPT4All(GTP_MODEL_PATH, allow_download=False)
    ).run()
