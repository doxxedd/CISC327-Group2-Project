import curses
import time
import getpass


class Dashboard:
    def __init__(self, stdscr, username):
        self.stdscr = stdscr
        self.username = username

    def display(self):
        self.stdscr.clear()
        self.stdscr.addstr(2, 1, f"Welcome, {self.username}!")
        self.stdscr.addstr(4, 1, "Dashboard")
        while True:
            self.stdscr.addstr(6, 1, f"Current Time: {time.strftime('%H:%M:%S')}")
            self.stdscr.refresh()
            time.sleep(1)


def landing_page(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    stdscr.addstr(2, 1, "Please log in:")
    stdscr.addstr(4, 1, "Username: ")
    stdscr.addstr(5, 1, "Password: ")

    username = stdscr.getstr(4, 11).decode()
    password = getpass.getpass(prompt="", stream=stdscr)

    # Verify the username and password (you can implement your authentication logic here)
    if username == "test" and password == "test":
        dash = Dashboard(stdscr, username)
        dash.display()
    else:
        stdscr.addstr(8, 1, "Invalid credentials. Press any key to exit.")
        stdscr.getch()

    return username, password
