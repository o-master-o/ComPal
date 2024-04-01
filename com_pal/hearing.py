from abc import ABC, abstractmethod

import speech_recognition


class Hearing(ABC):

    @abstractmethod
    def listen(self, output_file_path):
        pass


class SpeechRecognitionHearing(Hearing):

    def __init__(self):
        self.source = speech_recognition.Microphone()
        self.recognizer = speech_recognition.Recognizer()

    def listen(self, output_file_path):
        with self.source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(self.source)
            audio = self.recognizer.listen(self.source)
        try:
            with open(output_file_path, "wb") as f:
                f.write(audio.get_wav_data())
        except speech_recognition.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except speech_recognition.RequestError:
            print("Unable to access the Google Speech Recognition API.")
            return None
