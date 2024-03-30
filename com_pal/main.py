import os
import sys
import time

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


# global tasks
# global listeningToTask
# global askingAQuestion
global should_run
global listening_for_trigger_word

wake_word = ''
tasks = []
listeningToTask = False
askingAQuestion = False


def speak_text(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    fp = BytesIO()
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


def respond(text):
    engine.say(text)
    engine.runAndWait()


def listen_for_command():
    with source as s:
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


# def perform_command(command):
#     global tasks
#     global listeningToTask
#     global askingAQuestion
#     global should_run
#     global listening_for_trigger_word
#     if command:
#         print("Command: ", command)
#         if listeningToTask:
#             tasks.append(command)
#             listeningToTask = False
#             respond("Adding " + command + " to your task list. You have " + str(len(tasks)) + " currently in your list.")
#         elif "add a task" in command:
#             listeningToTask = True
#             respond("Sure, what is the task?")
#         elif "list tasks" in command:
#             respond("Sure. Your tasks are:")
#             for task in tasks:
#                 respond(task)
#         elif "take a screenshot" in command:
#             pyautogui.screenshot("screenshot.png")
#             respond("I took a screenshot for you.")
#         elif "open chrome" in command:
#             respond("Opening Chrome.")
#         elif "ask a question" in command:
#             askingAQuestion = True
#             respond("What's your question?")
#             return
#         elif askingAQuestion:
#             askingAQuestion = False
#             respond("Thinking...")
#             print("User command: ", command)
#             output = model.generate(command, max_tokens=200)
#             print("Output: ", output)
#             respond(output)
#         elif "exit" in command:
#             should_run = False
#         else:
#             respond("Sorry, I'm not sure how to handle that command.")
#     listening_for_trigger_word = True


# def main():
#     global listening_for_trigger_word
#     while should_run:
#         command = listen_for_command()
#         if listening_for_trigger_word:
#             listening_for_trigger_word = False
#         else:
#             perform_command(command)
#         time.sleep(1)
#     respond("Goodbye.")


if __name__ == "__main__":
    # main()
    print(listen_for_command())
