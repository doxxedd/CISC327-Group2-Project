import curses
import threading
import time
import landingpage
import pyautogui as p
import dashboard
dict = {}


def create_instance(stdscr):
    keyboard_thread = threading.Thread(target=worker)
    keyboard_thread.start()
    keyboard_thread.join()
    landingpage.landing_page(stdscr)


def worker():
    time.sleep(4)
    login()
    create_task("title", "details")
    create_project("title", "details")
    modify_task("new title", "new details")
    modify_project("new project title")
    view_task()
    view_project()
    remove_task()
    remove_project()
    logout()


def login():
    # as test:test
    for _ in range(2):
        p.keyUp('Fn')
        p.typewrite("test\n")
    dict["login"] = landingpage.testresult


def create_task(title, details):
    """creates task with given title and details. today's deadline
    """
    p.keyUp('Fn')
    p.typewrite(f"{title}\n{details}\n")
    # Deadline is always today in this test
    p.press('enter', presses=2)
    dict["create_task"] = dashboard.test


def create_project(title, details):
    """creates project with given title and details. today's deadline
    """
    p.press("down", presses=3)
    p.press("enter")
    p.keyUp('Fn')
    p.typewrite(f"{title}\n{details}\n")
    p.press("enter")
    dict["create_project"] = dashboard.test


def modify_task(title, details):
    """modifies task title and details
    """
    p.press("up", presses=2)
    p.press("enter")
    p.press("1")
    p.press("enter")
    p.keyUp('Fn')
    p.typewrite(f"{title}\n{details}\n\n")
    dict["modify_task"] = dashboard.test


def modify_project(title):
    """changes title and assign first task to project
    """
    p.press("down", presses=3)
    p.press("enter")
    p.press("1")
    p.press("enter")
    p.press("1")
    p.press("enter")
    p.keyUp('Fn')
    p.typewrite(f"{title}\n\n1\n4\n1\n")
    dict["modify_project"] = dashboard.test


def view_task():
    """views first task in list
    """
    p.press("down", presses=2)
    p.press("enter", presses=3)
    p.press("q")


def view_project():
    """views first project in list
    """
    p.press("down")
    p.press("enter")
    p.press("1")
    p.press("enter", presses=2)


def remove_task():
    p.press("up", presses=5)
    p.press("enter")
    p.press("1")
    p.press("enter")


def remove_project():
    p.press("down", presses=3)
    p.press("enter")
    p.press("1")
    p.press("enter")


def logout():
    p.press("down", presses=3)
    p.press("enter", presses=3)


def main():
    curses.wrapper(create_instance)


if __name__ == "__main__":
    main()
