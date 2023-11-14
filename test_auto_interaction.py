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
    modify_task("new title", "new details")
    modify_project("new project title", "new project detailss")


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
    p.press("up", presses=2)
    p.press("enter")
    p.press("1")
    p.press("enter")
    p.typewrite(f"{title}\n{details}\n\n")


def modify_project(title, details):
    p.press("down", presses=3)
    p.press("enter")
    p.press("1")
    p.press("enter")
    p.typewrite(f"{title}\n")
    


if __name__ == "__main__":
    curses.wrapper(create_instance)
