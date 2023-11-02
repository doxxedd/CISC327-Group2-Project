"""
Code for dashboard where user is prompted to choose from various action options
"""
import sqlite3
import curses
import core_objects
import landingpage
import shared
import datetime
import calendar
import time

def update_live_clock(stdscr):
    while True:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        stdscr.addstr(0, 0, f'Time: {current_time}', curses.color_pair(2))
        stdscr.refresh()
        time.sleep(1)

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

def display_calendar(stdscr):
    stdscr.clear()
    stdscr.refresh()

    # Get the current date
    today = datetime.date.today()
    current_date = today

    selected_date = None

    while True:
        # Clear the screen and draw the calendar
        stdscr.clear()

        # Display the month and year
        header = f'{current_date.strftime("%B %Y")}'
        stdscr.addstr(1, 2, header, curses.A_BOLD)

        # Display the days of the week
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days_of_week):
            stdscr.addstr(3, 4 + 4 * i, day, curses.A_BOLD)

        # Display the days of the month
        first_day = current_date.replace(day=1)
        last_day = current_date.replace(day=calendar.monthrange(current_date.year, current_date.month)[1])

        for day in range((last_day - first_day).days + 1):
            date = first_day + datetime.timedelta(days=day)
            row = (day + first_day.weekday()) // 7 + 4
            col = (day + first_day.weekday()) % 7

            if date == today:
                stdscr.addstr(row, 4 + 4 * col, date.strftime("%d"), curses.color_pair(1) | curses.A_BOLD)
            elif date == current_date:
                stdscr.addstr(row, 4 + 4 * col, date.strftime("%d"), curses.color_pair(2) | curses.A_BOLD)
            else:
                stdscr.addstr(row, 4 + 4 * col, date.strftime("%d"))

        if selected_date is not None:
            stdscr.addstr(12, 2, "Selected Date: " + selected_date.strftime("%Y-%m-%d"), curses.A_BOLD)

        stdscr.refresh()

        # Listen for user input
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_RIGHT:
            current_date += datetime.timedelta(days=1)
        elif key == curses.KEY_LEFT:
            current_date -= datetime.timedelta(days=1)
        elif key == 10:  # Enter key (select date)
            selected_date = current_date
            break

    return selected_date



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
        field3 = display_calendar(stdscr)
        if option == "Create Task":
            task = core_objects.Task()
            task.create_task(field1, field2, field3)

    if option in projectoptions:
        field1 = get_input(stdscr, "", 10, 35)
        field2 = get_input(stdscr, "", 12, 35)
        field3 = display_calendar(stdscr)
        if option == "Create Project":
            project = core_objects.Project()
            project.create_project(field1, field2, field3)

    if field1 == "test" and field2 == "test" and field3 == "test":
        stdscr.addstr(18, 35, "success!", curses.A_BOLD)
    else:
        stdscr.addstr(18, 30, "invalid field(s)!", curses.A_BOLD)
    stdscr.clear()
    stdscr.refresh()



def dashboard(stdscr):
    """
    Function to display dashboard for the user
    :return: None
    """
    stdscr.clear()
    stdscr.refresh()
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
        stdscr.refresh()
        


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
        

        # Display tasks in the timeline bar
        taskslist = shared.user.get_user_tasks()
        newlist = {}
        for task in taskslist:

            task = list(task)
            taskinfo = list(shared.user.get_task_details(task[0]))
            del taskinfo[0]
            del taskinfo[1]
            newlist[taskinfo[0]] = taskinfo[1]
        sorted_list = sorted(newlist.items(), key=lambda x:x[1])
        

        # Display tasks in the timeline bar
        if sorted_list:
            max_displayed_tasks = min(curses.LINES - 2, len(sorted_list))
            timeline_x = 2  # Adjust this value to set the left margin
            timeline_y = max(1, (curses.LINES - max_displayed_tasks) // 2)  # Adjust this value to set the vertical center

            # Add the timeline title
            title_x = 2  # Adjust this value to set the left margin
            title_y = max(0, (curses.LINES - max_displayed_tasks) // 2 - 1)  # Place it above the timeline
            stdscr.addstr(title_y, title_x, "Timeline", curses.A_UNDERLINE)

            for task_name, deadline in sorted_list[:max_displayed_tasks]:
                task_info = f"{task_name} ({deadline})"
                stdscr.addstr(timeline_y, timeline_x, task_info, curses.A_BOLD)
                timeline_y += 1
        # stdscr.refresh()

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
                tasks = shared.user.get_user_tasks()  # Fetch user's tasks
                if tasks:
                    stdscr.addstr(5, 30, "Select a task to modify:")
                    for i, task in enumerate(tasks, start=1):
                        stdscr.addstr(5 + i, 32, f"{i}. {task[1]}")
                    stdscr.refresh()
                    # Get user input for task selection
                    task_selection = get_input(stdscr, "Enter the number of the task to modify (or press 'Enter' to go back): ", 10 + len(tasks), 35)
                    stdscr.clear()   
                    if task_selection.isnumeric():
                        task_selection = int(task_selection)
                        if 1 <= task_selection <= len(tasks):
                            # Fetch task details
                            selected_task_id = tasks[task_selection - 1][0]
                            task_details = list(shared.user.get_task_details(selected_task_id))
                            if task_details:
                                # Display task details and get updated values from the user
                                stdscr.addstr(10, 30, "Task Details:")
                                stdscr.addstr(11, 32, f"Title: {task_details[1]}")
                                stdscr.addstr(12, 32, f"Details: {task_details[2]}")
                                stdscr.addstr(13, 32, f"Deadline: {task_details[3]}")

                                new_title = get_input(stdscr, "New Title (or press 'Enter' to keep the current value): ", 15, 32)
                                new_details = get_input(stdscr, "New Details (or press 'Enter' to keep the current value): ", 16, 32)
                                new_deadline = display_calendar(stdscr)

                                # Check if input is empty (i.e., user pressed 'Enter')
                                new_tasks = task_details
                                if new_title:
                                    new_tasks[1] = new_title
                                if new_details:
                                    new_tasks[2] = new_details
                                if new_deadline:
                                    new_tasks[3] = new_deadline

                                # Update the task
                                shared.user.update_task(selected_task_id, new_tasks[1], new_tasks[2], new_tasks[3])
                                stdscr.addstr(19, 30, "Task modified successfully.", curses.A_BOLD)
                            else:
                                stdscr.addstr(19, 30, "Task not found or doesn't belong to you.", curses.A_BOLD)
                        else:
                            stdscr.addstr(19, 30, "Invalid task selection.", curses.A_BOLD)
                            
                    else:
                        stdscr.addstr(19, 30, "Invalid input. Please enter a valid task number or 'B' to go back.", curses.A_BOLD)
                else:
                    stdscr.addstr(5, 30, "No tasks found to modify.")
                    
            elif selected_row == 2:
                tasks = shared.user.get_user_tasks()  # Fetch user's tasks
                if tasks:
                    stdscr.addstr(5, 30, "Select a task to modify:")
                    for i, task in enumerate(tasks, start=1):
                        stdscr.addstr(5 + i, 32, f"{i}. {task[1]}")
                    stdscr.refresh()
                    # Get user input for task selection
                    task_selection = get_input(stdscr, "Enter the number of the task to delete(or press 'Enter' to go back): ", 10 + len(tasks), 35)
                    stdscr.clear()   
                    if task_selection.isnumeric():
                        task_selection = int(task_selection)
                        if 1 <= task_selection <= len(tasks):
                            # Fetch task details
                            selected_task_id = tasks[task_selection - 1][0]
                            shared.user.remove_task_from_db(selected_task_id)
                            stdscr.addstr(19, 30, "Task deleted successfully.", curses.A_BOLD)
                        else:
                            time.sleep
                            stdscr.addstr(19, 30, "Invalid task selection.", curses.A_BOLD)
                    else:
                        stdscr.addstr(19, 30, "Invalid input. Please enter a valid task number or 'B' to go back.", curses.A_BOLD)
                else:
                    stdscr.addstr(5, 30, "No tasks found to delete.")
            elif selected_row == 3:
                create_field_page(stdscr, "Create Project", "title", "details", "deadline")
            elif selected_row == 4:
                create_field_page(stdscr, "Modify Project", "title", "details", "deadline")
            elif selected_row == 5:
                stdscr.addstr(5, 30, "You chose 'Remove Project'")
            stdscr.clear()
            stdscr.refresh()
            

