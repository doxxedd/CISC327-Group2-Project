import curses
import time
import dashboard


def set_terminal_size(rows, cols):
    stdscr = curses.initscr()
    curses.resizeterm(rows, cols)  # Set the terminal size
    stdscr.refresh()
    return stdscr


def get_center_x(prompt):
    return int((curses.COLS - len(prompt)) / 2)


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


def show_title(stdscr):
    title = "Tasker"
    title_y, title_x = 1, int((curses.COLS - len(title)) / 2)
    stdscr.addstr(title_y, title_x, title, curses.color_pair(1))


def show_time(stdscr):
    current_time = time.strftime('%H:%M:%S')
    time_y, time_x = 1, curses.COLS - len(current_time) - 1
    stdscr.addstr(time_y, time_x, current_time, curses.color_pair(2))


def landing_page(stdscr):
    # set_terminal_size(1200, 1000)
    curses.curs_set(1)
    stdscr.clear()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    show_time(stdscr)
    show_title(stdscr)
    stdscr.refresh()

    login_form = [["Username: ", ""], ["Password: ", ""]]

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
