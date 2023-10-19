import curses
import datetime
from curses.textpad import Textbox, rectangle


def dashboard(stdscr):
    stdscr.clear()
 # Set up colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    options = ["Create Task", "Modify Task", "Remove Task"]
    selected_row = 0

    curses.curs_set(0)  # Hide the cursor

    while True:
        stdscr.clear()

        # Display the menu options
        height, width = stdscr.getmaxyx()
        for idx, option in enumerate(options):
            x = width // 2 - len(option) // 2
            y = height // 2 - len(options) // 2 + idx
            if idx == selected_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and selected_row > 0:
            selected_row -= 1
        elif key == curses.KEY_DOWN and selected_row < len(options) - 1:
            selected_row += 1
        elif key == 10:  # Enter key
            # Execute the selected option
            stdscr.clear()
            if selected_row == 0:
                # Create Task
                stdscr.addstr(5, 0, "You chose 'Create Task'")
            elif selected_row == 1:
                # Modify Task
                stdscr.addstr(5, 0, "You chose 'Modify Task'")
            elif selected_row == 2:
                # Remove Task
                stdscr.addstr(5, 0, "You chose 'Remove Task'")
            stdscr.refresh()
            stdscr.getch()  # Wait for a key press before returning to the menu

