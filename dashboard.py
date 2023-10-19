import curses
import time
import getpass


def set_terminal_size(rows, cols):
    stdscr = curses.initscr()
    curses.resizeterm(rows, cols)  # Set the terminal size
    stdscr.refresh()
    return stdscr


def landing_page(stdscr):
    # set_terminal_size(1200, 1000)
    stdscr.clear()
    curses.curs_set(0)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    title = "Tasker"
    title_y, title_x = 2, int((curses.COLS - len(title)) / 2)

    current_time = time.strftime('%H:%M:%S')
    time_y, time_x = 1, curses.COLS - len(current_time) - 1


    username = ""
    password = ""
    username_label = "Username: "
    password_label = "Password: "

    active_input = username

    while True:
        stdscr.clear()

        # Display title
        stdscr.addstr(title_y, title_x, title, curses.color_pair(1))

        # Draw username input box
        stdscr.addstr(title_y + 2, title_x, username_label)
        stdscr.addstr(title_y + 2, title_x + len(username_label), username, curses.color_pair(2))

        # Draw password input box (hide the password with asterisks)
        stdscr.addstr(title_y + 3, title_x, password_label)
        stdscr.addstr(title_y + 3, title_x + len(password_label), '*' * len(password), curses.color_pair(2))

        if active_input == username:
            stdscr.move(title_y + 2, title_x + len(username) + len(username_label))
        else:
            stdscr.move(title_y + 3, title_x + len(password) + len(password_label))

        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        if key == curses.KEY_ENTER:  # Enter key
            active_input = password  # Change the active input to password
        elif key == curses.KEY_BACKSPACE:
            if active_input == username:
                username = username[:-1]
            else:
                password = password[:-1]
        else:
            if active_input == username:
                username += chr(key)
            else:
                password += chr(key)