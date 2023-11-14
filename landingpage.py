"""
User landing page where user is prompted for login details
"""
import curses
import time
import dashboard
import sqlite3
from core_objects import User
import shared

testresult = None

def register_user(username, password):
    """
    Function to register user into system
    :param username: user's username
    :param password: user's password
    :return: True if successful, False otherwise
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return False  # Username already exists, registration failed

    # If the username is unique, insert the new user into the database
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()
    return True  # Registration successful

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

def validate_user(username, password):
    """
    Function to verify user credential in database when logging in
    """
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # check database
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    conn.close()
    testresult = True

    return user is not None


def landing_page(stdscr):
    """
    Function to display landing page
    :return: None
    :rtype:
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            details TEXT,
            deadline TEXT,
            completed BOOLEAN,
            deleted BOOLEAN,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Create Project table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            details TEXT,
            deadline TEXT,
            completed BOOLEAN,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            task_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')

    conn.commit()
    conn.close()
    # set_terminal_size(1200, 1000)
    while True:
        
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

        # Check for login
        user_exists = validate_user(username, password)
        if username == "" and password == "":
            break

        if user_exists:
            stdscr.addstr(9, get_center_x("Login successful!"), "Login successful!", curses.A_BOLD)

            shared.user = User()
            if shared.user.login_user(username, password):
                dashboard.testresult.append("Login successful")
            dashboard.dashboard(stdscr)
            break  # Exit the loop if login is successful
        else:
            curses.curs_set(0)
            stdscr.addstr(9, get_center_x("Login failed."), "Login failed.", curses.A_BOLD)

        dashboard.testresult.append("Login failed")
        stdscr.addstr(11, get_center_x("Press 'R' to retry or 'C' to register."), "Press 'R' to retry or 'C' to register.", curses.A_BOLD)
        stdscr.refresh()
        action = stdscr.getch()

        if action == ord('C') or action == ord('c'):
            # User chose to register, proceed with registration
            registration_success = register_user(username, password)
            if registration_success:
                dashboard.testresult.append("Registration successful")
                stdscr.addstr(9, get_center_x("Registration successful!"), "Registration successful!", curses.A_BOLD)
            else:
                dashboard.testresult.append("Registration failed")
                curses.curs_set(0)
                stdscr.addstr(9, get_center_x("Registration failed. Username already exists."), "Registration failed. Username already exists.", curses.A_BOLD)

    conn.close()
    stdscr.refresh()
    stdscr.getch()