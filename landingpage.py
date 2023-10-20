"""
User landing page where user is prompted for login details
"""
import curses
import time
import dashboard


def set_terminal_size(rows, cols):
    """
    Function to set size of terminal displayed
    :param rows: Row size of terminal
    :param cols: Column size of terminal
    :return: stdscr
    """
    stdscr = curses.initscr()
    curses.resizeterm(rows, cols)  # Set the terminal size
    stdscr.refresh()
    return stdscr


def get_center_x(prompt):
    """
    Function to find center column value for terminal size based on the length of the prompt to be displayed
    :param prompt: Text prompt to be displayed
    :return: Coordinate of center x value
    """
    return int((curses.COLS - len(prompt)) / 2)


def display_form_element(stdscr, prompt, value, row, col):
    """
    Function to displays element that needs user input
    :param prompt: Text to display as prompt for input
    :param value: User input
    :param row: Row coordinate for where to display element on screen
    :param col: Column coordinate for where to display element on screen
    :return: None
    """
    stdscr.addstr(row, col, prompt)
    stdscr.addstr(row, col + len(prompt), value)


def get_input(stdscr, prompt, row, col):
    """
    Function to allow user to type input
    :param prompt: Text to display as prompt for input
    :param row: Row coordinate for where to display element on screen
    :param col: Column coordinate for where to display element on screen
    :return: Value that was inputted
    """
    stdscr.addstr(row, col, prompt)
    stdscr.refresh()
    input_window = curses.newwin(1, 30, row, col + len(prompt))
    input_window.keypad(True)

    curses.echo()
    input_window.refresh()
    value = input_window.getstr(0, 0).decode('utf-8')
    curses.noecho()

    return value


def show_title(stdscr):
    """
    Function to display application title on landing page
    :return: None
    """
    title = "Tasker"
    # display in the center of the screen
    title_y, title_x = 1, int((curses.COLS - len(title)) / 2)
    stdscr.addstr(title_y, title_x, title, curses.color_pair(1))


def show_time(stdscr):
    """
    Function to display time on landing page
    :return: None
    """
    # get current time
    current_time = time.strftime('%H:%M:%S')
    # display on top right of screen
    time_y, time_x = 1, curses.COLS - len(current_time) - 1
    stdscr.addstr(time_y, time_x, current_time, curses.color_pair(2))


def landing_page(stdscr):
    """
    Function to display landing page
    :return: None
    :rtype:
    """
    # set_terminal_size(1200, 1000)
    curses.curs_set(1)
    stdscr.clear()

    # initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # display the time
    show_time(stdscr)

    # display title
    show_title(stdscr)
    stdscr.refresh()

    # list of prompts
    login_form = [["Username: ", ""], ["Password: ", ""]]

    # display prompts and input fields
    current_row = 5
    for label, value in login_form:
        display_form_element(stdscr, label, value, current_row, 2)
        current_row += 2

    # Get user input for username and password
    username = get_input(stdscr, "", 5, len(login_form[0][0]) + 2)
    password = get_input(stdscr, "", 7, len(login_form[1][0]) + 2)

    # Check for login (demo always allows access)
    if username == "test" and password == "test":
        stdscr.addstr(9, get_center_x("Login successful!"), "Login successful!", curses.A_BOLD)
        dashboard.dashboard(stdscr)
    else:
        curses.curs_set(0)
        stdscr.addstr(9, get_center_x("Login failed."), "Login failed.", curses.A_BOLD)

    stdscr.refresh()
    stdscr.getch()
