import curses
import threading
import time
import landingpage
import pyautogui as p


def create_instance(stdscr):
    keyboard_thread = threading.Thread(target=worker)
    keyboard_thread.start()
    keyboard_thread.join()
    landingpage.landing_page(stdscr)


def worker():
    login()


def login():
    time.sleep(2)
    for _ in range(2):
        p.typewrite("test")
        p.press('enter')


def create_task():
    pass


if __name__ == "__main__":
    curses.wrapper(create_instance)
