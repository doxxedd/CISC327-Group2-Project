"""This python file aims to mimic interaction of a user using their keyboard to
interact with this program. We can use the sequence of keystrokes to test the
program.
"""

import subprocess
import pyautogui as p


p.PAUSE = 0.3  # delay keystrokes by 0.3s after each call


def create_instance():
    """runs an instance of the program
    """
    try:
        subprocess.run('python3 main.py', check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error {e}")


def login():
    for _ in range(2):
        p.typewrite("test")
        p.press('enter')


if __name__ == "__main__":
    create_instance()
