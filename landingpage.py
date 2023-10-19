import curses
import time
import dashboard
from curses.textpad import Textbox, rectangle


def set_terminal_size(rows, cols):
    stdscr = curses.initscr()
    curses.resizeterm(rows, cols)  # Set the terminal size
    stdscr.refresh()
    return stdscr


def display_form_element(stdscr, prompt, value, row, col):
    stdscr.addstr(row, col, prompt)
    stdscr.addstr(row, col + len(prompt), value)


def get_input(stdscr, prompt, row, col):
    stdscr.addstr(row, col, prompt)
    stdscr.refresh()
    input_window = curses.newwin(1, 30, row, col + len(prompt))
    input_window.keypad(True)

    curses.echo()
    input_window.refresh()
    value = input_window.getstr(0, 0).decode('utf-8')
    curses.noecho()

    return value


def landing_page(stdscr):
    # set_terminal_size(1200, 1000)
    curses.curs_set(1)
    stdscr.clear()
    stdscr.refresh()

    login_form = [
        ("Username: ", ""),
        ("Password: ", "")
    ]

    current_row = 5
    for label, value in login_form:
        display_form_element(stdscr, label, value, current_row, 10)
        current_row += 2

    # Get user input for username and password
    username = get_input(stdscr, "", 5, 20)
    password = get_input(stdscr, "", 7, 20)

    # Check for login (demo always allows access)
    if username == "test" and password == "test":
        stdscr.addstr(9, 10, "Login successful!", curses.A_BOLD)
        dashboard.dashboard(stdscr)
    else:
        stdscr.addstr(9, 10, "Login failed. Please try again.", curses.A_BOLD)

    stdscr.refresh()
    stdscr.getch()

