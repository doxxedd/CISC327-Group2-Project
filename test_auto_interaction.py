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
    time.sleep(1)
    login()
    create_task("title", "detaillssss")


def login():
    for _ in range(2):
        p.typewrite("test\n")


def create_task(title, details):
    p.typewrite(f"{title}\n")
    p.typewrite(f"{details}\n")

    time.sleep(0.5)
    # Deadline is always 3 days in the future in this test
    for _ in range(5):
        p.press('right')
    p.press('enter')

if __name__ == "__main__":
    curses.wrapper(create_instance)
