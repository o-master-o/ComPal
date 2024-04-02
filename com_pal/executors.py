from pathlib import Path
import pyautogui
import datetime


def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")


class Executor:

    def make_screenshot(self):
        path_to_save = Path.home() / f'Downloads/Screenshot_{timestamp()}.png'
        pyautogui.screenshot(path_to_save)
        return path_to_save
