import os
from abc import ABC, abstractmethod

import whisper


class SpeechRecognition(ABC):

    @abstractmethod
    def transcript(self, audio):
        pass


class OpenaiWhisper(SpeechRecognition):

    def __init__(self, model_path):
        self.model_path = model_path
        self.model = whisper.load_model(os.path.expanduser(self.model_path))

    def transcript(self, audio):
        output = self.model.transcribe(audio, fp16=False)
        if output and output['text']:
            print("You said:", output['text'])
            return output['text'].lower()
        return None
