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

testresult = []


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
    """Function that displays calender when selecting deadline

    Returns:
        string: selected date
    """
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
            return "Task Created Successfully"

    if option in projectoptions:
        field1 = get_input(stdscr, "", 10, 35)
        field2 = get_input(stdscr, "", 12, 35)
        field3 = display_calendar(stdscr)
        if option == "Create Project":
            project = core_objects.Project()
            project.create_project(field1, field2, field3)
            return "Project Created Successfully"

    if field1 == "test" and field2 == "test" and field3 == "test":
        stdscr.addstr(18, 35, "success!", curses.A_BOLD)
    else:
        stdscr.addstr(18, 30, "invalid field(s)!", curses.A_BOLD)
        return "Task not created"
    stdscr.clear()
    stdscr.refresh()


def task_modifier(stdscr):
    """
    Displays and updates task details (updates db too)
    """
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
                    return "Task Modified Successfully"
                else:
                    stdscr.addstr(19, 30, "Task not found or doesn't belong to you.", curses.A_BOLD)
            else:
                stdscr.addstr(19, 30, "Invalid task selection.", curses.A_BOLD)

        else:
            stdscr.addstr(19, 30, "Invalid input. Please enter a valid task number or 'B' to go back.", curses.A_BOLD)
    else:
        stdscr.addstr(5, 30, "No tasks found to modify.")
        return "No tasks found to modify"


def task_deleter(stdscr):
    """
    Removes task from displaying and db
    """
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
                return "Task Deleted Successfully"
            else:
                stdscr.addstr(19, 30, "Invalid task selection.", curses.A_BOLD)
        else:
            stdscr.addstr(19, 30, "Invalid input. Please enter a valid task number or 'B' to go back.", curses.A_BOLD)
    else:
        stdscr.addstr(5, 30, "No tasks found to delete.")
        return "No Tasks Found to Delete"


def task_viewer(stdscr):
    """
    Allows user to select and view a task
    """
    tasks = shared.user.get_user_tasks()  # Fetch user's tasks

    if not tasks:
        stdscr.addstr(0, 0, "No tasks found.")
        stdscr.refresh()
        stdscr.getch()  # Wait for user input
        return

    selected_task = 0  # Initially select the first task

    while True:
        stdscr.clear()

        # Display the list of tasks
        for i, task in enumerate(tasks, start=1):
            if i - 1 == selected_task:
                stdscr.addstr(2 + i, 1, f"{i}. {task[1]}", curses.A_REVERSE)
            else:
                stdscr.addstr(2 + i, 1, f"{i}. {task[1]}")

        stdscr.addstr(0, 0, "Task Viewer", curses.A_BOLD)
        stdscr.addstr(1, 0, "Use arrow keys to navigate, 'Enter' to view a task, 'q' to exit.")

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            break  # Exit task viewer
        elif key == 10:  # Enter key
            # Display the details of the selected task
            task_details = shared.user.get_task_details(tasks[selected_task][0])
            stdscr.clear()
            stdscr.addstr(0, 0, "Task Details", curses.A_BOLD)

            if task_details:
                stdscr.addstr(2, 0, f"Title: {task_details[1]}")
                stdscr.addstr(3, 0, f"Details: {task_details[2]}")
                stdscr.addstr(4, 0, f"Deadline: {task_details[3]}")
            else:
                stdscr.addstr(2, 0, "Task not found or doesn't belong to you.")
                return "Task Not Found"

            stdscr.addstr(7, 0, "Press 'Enter' to go back to the task list.")
            stdscr.refresh()

            while True:
                key = stdscr.getch()
                if key == 10:  # Enter key
                    break  # Go back to the task list

        elif key == curses.KEY_UP and selected_task > 0:
            selected_task -= 1
        elif key == curses.KEY_DOWN and selected_task < len(tasks) - 1:
            selected_task += 1
    return "Tasks viewed Successfully"


def project_deleter(stdscr):
    """
    Allows user to delete a project
    """
    projects = shared.user.get_user_projects()  # Fetch user's projects
    if projects:
        stdscr.addstr(5, 30, "Your Projects:")
        for i, project in enumerate(projects, start=1):
            stdscr.addstr(5 + i, 32, f"{i}. {project[1]}")
        stdscr.refresh()
        # Get user input for project selection
        project_selection = get_input(stdscr, "Enter the number of the project to Delete (or press 'Enter' to go back): ", 10 + len(projects), 35)
        stdscr.clear()
        if project_selection.isnumeric():
            project_selection = int(project_selection)
            if 1 <= project_selection <= len(projects):
                # Fetch project details
                selected_project_id = projects[project_selection - 1][0]
                project_details = shared.user.remove_project(selected_project_id)
                return "Project Deleted Successfully"
            else:
                stdscr.addstr(14, 32, "Invalid project selection.")
        else:
            stdscr.addstr(14, 32, "Invalid input. Please enter a valid project number or 'B' to go back.", curses.A_BOLD)
    else:
        stdscr.addstr(5, 30, "No projects found.")
        return "No Projects Found to Delete"


def project_viewer(stdscr):
    """
    Allows user to select and view a project
    """
    projects = shared.user.get_user_projects()  # Fetch user's projects
    if projects:
        stdscr.addstr(5, 30, "Your Projects:")
        for i, project in enumerate(projects, start=1):
            stdscr.addstr(5 + i, 32, f"{i}. {project[1]}")
        stdscr.refresh()
        # Get user input for project selection
        project_selection = get_input(stdscr, "Enter the number of the project to view (or press 'Enter' to go back): ", 10 + len(projects), 35)
        stdscr.clear()
        if project_selection.isnumeric():
            project_selection = int(project_selection)
            if 1 <= project_selection <= len(projects):
                # Fetch project details
                selected_project_id = projects[project_selection - 1][0]
                project_details = shared.user.get_project_details(selected_project_id)
                if project_details:
                    # Display project details
                    stdscr.addstr(10, 30, "Project Details:")
                    stdscr.addstr(11, 32, f"Title: {project_details[1]}")
                    stdscr.addstr(12, 32, f"Details: {project_details[2]}")
                    stdscr.addstr(13, 32, f"Deadline: {project_details[3]}")
                    stdscr.addstr(14, 32, "Tasks in this project:")

                    # Fetch tasks associated with the project
                    project_tasks = shared.user.get_tasks_in_project(selected_project_id)
                    for i, task in enumerate(project_tasks, start=1):
                        stdscr.addstr(14 + i, 34, f"{i}. {task[1]}")

                    stdscr.addstr(16 + len(project_tasks), 32, "Press 'Enter' to go back.")
                    stdscr.refresh()

                    key = stdscr.getch()
                    return "Project Viewed Successfully"

                    if key == 10:  # Enter key (go back)
                        pass
                else:
                    stdscr.addstr(14, 32, "Project not found or doesn't belong to you.")
            else:
                stdscr.addstr(14, 32, "Invalid project selection.")
        else:
            stdscr.addstr(14, 32, "Invalid input. Please enter a valid project number or 'B' to go back.", curses.A_BOLD)
    else:
        stdscr.addstr(5, 30, "No projects found.")
        return "Project Not Found"


def project_modifier(stdscr):
    """
    Displays and updates project details (updates db too)
    """
    stdscr.addstr(5, 30, "You chose 'Modify Project'")
    stdscr.addstr(6, 32, "Select a project to modify:")

    # Fetch the user's projects
    projects = shared.user.get_user_projects()

    if projects:
        for i, project in enumerate(projects, start=1):
            stdscr.addstr(6 + i, 32, f"{i}. {project[1]}")
        stdscr.refresh()

        # Get user input for project selection
        project_selection = get_input(stdscr, "Enter the number of the project to modify (or press 'Enter' to go back): ", 7 + len(projects), 32)
        stdscr.clear()

        if project_selection.isnumeric():
            project_selection = int(project_selection)
            if 1 <= project_selection <= len(projects):
                # Fetch project details
                selected_project_id = projects[project_selection - 1][0]
                project_details = list(shared.user.get_project_details(selected_project_id))

                if project_details:
                    # Display project details and allow the user to modify them
                    stdscr.addstr(10, 30, "Project Details:")
                    stdscr.addstr(11, 32, f"Title: {project_details[1]}")
                    stdscr.addstr(12, 32, f"Details: {project_details[2]}")
                    stdscr.addstr(13, 32, f"Deadline: {project_details[3]}")
                    stdscr.addstr(15, 32, "1. Change Project Title")
                    stdscr.addstr(16, 32, "2. Change Project Details")
                    stdscr.addstr(17, 32, "3. Change Project Deadline")
                    stdscr.addstr(18, 32, "4. Add Tasks to Project")
                    stdscr.addstr(19, 32, "5. Back")
                    stdscr.refresh()

                    option = get_input(stdscr, "Enter your choice: ", 21, 32)

                    if option == "1":
                        # Allow the user to change the project title
                        new_title = get_input(stdscr, "New Project Title: ", 23, 32)
                        # Update the project title in the database
                        shared.user.update_project(selected_project_id, new_title, project_details[2], project_details[3])
                        stdscr.addstr(26, 32, "Project title modified successfully.", curses.A_BOLD)
                        return "Project Title Modified successfully"
                    elif option == "2":
                        # Allow the user to change the project details
                        new_details = get_input(stdscr, "New Project Details: ", 23, 32)
                        # Update the project details in the database
                        shared.user.update_project(selected_project_id, project_details[1], new_details, project_details[3])
                        stdscr.addstr(26, 32, "Project details modified successfully.", curses.A_BOLD)
                        return "Project Details Modified successfully"
                    elif option == "3":
                        # Allow the user to change the project deadline
                        new_deadline = display_calendar(stdscr)
                        # Update the project deadline in the database
                        shared.user.update_project(selected_project_id, project_details[1], project_details[2], new_deadline)
                        stdscr.addstr(26, 32, "Project deadline modified successfully.", curses.A_BOLD)
                        return "Project Deadline Modified successfully"
                    elif option == "4":
                        stdscr.clear()
                        stdscr.addstr(5, 30, "You chose 'Add Tasks to Project'")

                        # Display a list of available tasks
                        tasks = shared.user.get_user_tasks()  # Fetch user's tasks
                        if tasks:
                            stdscr.addstr(6, 32, "Select tasks to add to the project (use space to select/deselect, press 'Enter' when done):")
                            task_selections = [False] * len(tasks)  # Initialize task selections as all False
                            current_row = 7

                            while True:
                                for i, (task_id, task_title) in enumerate(tasks):
                                    checkbox = "[X]" if task_selections[i] else "[ ]"
                                    stdscr.addstr(current_row + i, 32, f"{checkbox} {i + 1}. {task_title}")

                                stdscr.refresh()
                                key = stdscr.getch()

                                if key == ord('q'):
                                    break  # Exit if the user presses 'q'
                                elif key == 10:
                                    # User pressed 'Enter', finish task selection
                                    break
                                elif key in [curses.KEY_ENTER, 10]:
                                    # Handle the 'Enter' key as well
                                    break
                                elif 0 <= key - ord('1') < len(tasks):
                                    # Toggle task selection when a number key is pressed
                                    task_index = key - ord('1')
                                    task_selections[task_index] = not task_selections[task_index]

                            # Add the selected tasks to the project
                            selected_tasks = [task_id for i, (task_id, _) in enumerate(tasks) if task_selections[i]]
                            for task_id in selected_tasks:
                                shared.user.add_task_to_project(selected_project_id, task_id)

                            stdscr.addstr(7 + len(tasks), 32, "Tasks added to the project successfully.", curses.A_BOLD)
                        else:
                            stdscr.addstr(6, 32, "No tasks found to add to the project.")

                        stdscr.refresh()
                    elif option == "5":
                        # User chooses to go back
                        pass
                    else:
                        stdscr.addstr(26, 32, "Invalid choice. Please enter a valid option.", curses.A_BOLD)
                else:
                    stdscr.addstr(26, 32, "Project not found or doesn't belong to you.", curses.A_BOLD)
            else:
                stdscr.addstr(26, 32, "Invalid project selection.", curses.A_BOLD)
        else:
            stdscr.addstr(26, 32, "Invalid input. Please enter a valid project number or 'Enter' to go back.", curses.A_BOLD)
    else:
        stdscr.addstr(6, 32, "No projects found to modify.")
        return "Project Not Found to Modify"


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
               "Create Project", "Modify Project", "Remove Project", "View Tasks", "View Projects", "Logout"]

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
        sorted_list = sorted(newlist.items(), key=lambda x: x[1])

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
                result = create_field_page(stdscr, "Create Task", "title", "details", "deadline")
                testresult.append(result)
            elif selected_row == 1:
                result = task_modifier(stdscr)
                testresult.append(result)
            elif selected_row == 2:
                result = task_deleter(stdscr)
                testresult.append(result)
            elif selected_row == 3:
                result = create_field_page(stdscr, "Create Project", "title", "details", "deadline")
            elif selected_row == 4:
                result = project_modifier(stdscr)
                testresult.append(result)
            elif selected_row == 5:
                result = project_deleter(stdscr)
                testresult.append(result)
            elif selected_row == 6:
                result = task_viewer(stdscr)
                testresult.append(result)
            elif selected_row == 7:
                result = project_viewer(stdscr)
                testresult.append(result)
            elif selected_row == 8:
                if shared.user:
                    shared.user.logout_user()
                    break

    # Specify the new file name
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"Test_log_{timestamp}.txt"

    # Open the file in write mode
    with open(file_name, "w") as file:
        # Iterate over the strings and write each one as a line
        for string in testresult:
            if string != "none":
                file.write(f"{string} \n")
    landingpage.landing_page(stdscr)
