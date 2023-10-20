"""
Code for dashboard where user is prompted to choose from various action options
"""

import curses


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


def create_field_page(stdscr, option, field1, field2, field3):
    """
    General function to input fiels for tasks or projects
    :param option: Option selected by user (specific action for project or task)
    :param field1: Field prompt for input by user
    :param field2: Field prompt for input by user
    :param field3: Field prompt for input by user
    :return: None
    """
    curses.curs_set(1)
    stdscr.clear()
    stdscr.refresh()
    # Create Task
    stdscr.addstr(5, 30, f"You chose '{option}'")
    taskoptions = ["Create Task", "Modify Task", "Remove Task"]
    projectoptions = ["Create Project", "Modify Project", "Remove Project"]
    detail_form = [
        (f"{field1}: ", ""),
        (f"{field2}: ", ""),
        (f"{field3}: ", "")
    ]

    current_row = 10
    for label, value in detail_form:
        display_form_element(stdscr, label, value, current_row, 25)
        current_row += 2
    # Get user input for username and password

    if option in taskoptions:
        field1 = get_input(stdscr, "", 10, 35)
        field2 = get_input(stdscr, "", 12, 35)
        field3 = get_input(stdscr, "", 14, 35)

    if option in projectoptions:
        field1 = get_input(stdscr, "", 10, 35)
        field2 = get_input(stdscr, "", 12, 35)
        field3 = get_input(stdscr, "", 14, 35)

    if field1 == "test" and field2 == "test" and field3 == "test":
        stdscr.addstr(18, 35, "success!", curses.A_BOLD)
    else:
        stdscr.addstr(18, 30, "invalid field(s)!", curses.A_BOLD)

    stdscr.refresh()
    stdscr.getch()


def dashboard(stdscr):
    """
    Function to display dashboard for the user
    :return: None
    """
    stdscr.clear()
    # Set up colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    options = ["Create Task", "Modify Task", "Remove Task",
                "Create Project", "Modify Project", "Remove Project"]

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
                create_field_page(stdscr, "Create Task", "title", "details", "deadline")
            elif selected_row == 1:
                create_field_page(stdscr, "Modify Task", "title", "details", "deadline")
            elif selected_row == 2:
                stdscr.addstr(5, 30, "You chose 'Remove Task'")
            elif selected_row == 3:
                create_field_page(stdscr, "Create Project", "title", "details", "deadline")
            elif selected_row == 4:
                create_field_page(stdscr, "Modify Project", "title", "details", "deadline")
            elif selected_row == 5:
                stdscr.addstr(5, 30, "You chose 'Remove Project'")
            stdscr.refresh()
            stdscr.getch()
