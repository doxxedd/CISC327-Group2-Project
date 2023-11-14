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
    time.sleep(0.5)
    login()
    create_task("title", "details")
    create_project("title", "details")


def login():
    # as test:test
    for _ in range(2):
        p.typewrite("test\n")


def create_task(title, details):
    p.typewrite(f"{title}\n{details}\n")
    # Deadline is always today in this test
    p.press('enter', presses=2)

def create_project(title, details):
    p.press("down", presses=3)
    p.press("enter")
    p.typewrite(f"{title}\n{details}\n")
    p.press("enter")

def modify_task(title, details):
    pass

if __name__ == "__main__":
    curses.wrapper(create_instance)
