import datetime
import sqlite3
from shared import user
"""Backend classes to be used in next iterations of the prototype
"""
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
current_user = None


class User:
    """
    This class keeps track of user attributes
    """

    def __init__(self):
        self.username = None
        self.password = None
        self.data = Data()

    def save_user(self):
        """
        Function to save a user's username and password to the database
        """
        # save username and password
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (self.username, self.password))
        conn.commit()

    def get_user_tasks(self):
        """
        Function to get tasks associated to the current user from the database
        """
        # initialize list of tasks
        tasks = []
        # get task
        if self.user_id:
            cursor.execute('SELECT id, title FROM tasks WHERE user_id = ? AND deleted = 0', (self.user_id,))
            tasks = cursor.fetchall()

        return tasks
    
    def get_user_projects(self):
        """
        Function to get projects associated to the current user from the database
        """
        # initialize list of projects
        projects = []
        # get projects
        if self.user_id:
            cursor.execute('SELECT id, title FROM projects WHERE user_id = ?', (self.user_id,))
            tasks = cursor.fetchall()

        return tasks
    
    
    def get_task_details(self, task_id):
        """
        Function to get details of a specific task associated to the current user from the database using task id
        :param task_id: task id for specific task
        :return: task details
        """
        # initialize task details variable
        task_details = None
        # get details
        if self.user_id:
            cursor.execute('SELECT id, title, details, deadline FROM tasks WHERE id = ? AND user_id = ? AND deleted = 0', (task_id, self.user_id))
            task_details = cursor.fetchone()

        return task_details
    
    def get_project_details(self, project_id):
        """
        Function to get details of a specific project associated to the current user from the database using project id
        :param project_id: project id for specific project
        :return: project details
        """
        # initialize project details variable
        project_details = None
        if self.user_id:
            # get details
            cursor.execute('SELECT id, title, details, deadline FROM projects WHERE id = ? AND user_id = ?', (project_id, self.user_id))
            project_details = cursor.fetchone()

        return project_details
    
    def add_task_to_project(self, project_id, task_id):
        """
        Function to associate specific task with a specific project in database table
        :param project_id: project id for specific project
        :param task_id: task id for specific task
        """
        if self.user_id:
            # check if the project exists and belongs to the user
            cursor.execute('SELECT id FROM projects WHERE id = ? AND user_id = ?', (project_id, self.user_id))
            project = cursor.fetchone()
            if project:
                # check if the task exists and belongs to the user
                cursor.execute('SELECT id FROM tasks WHERE id = ? AND user_id = ?', (task_id, self.user_id))
                task = cursor.fetchone()
                if task:
                    # Check if the task is not already associated with the project
                    cursor.execute('SELECT id FROM project_tasks WHERE project_id = ? AND task_id = ?', (project_id, task_id))
                    existing_association = cursor.fetchone()
                    if not existing_association:
                        # Add the task to the project
                        cursor.execute('INSERT INTO project_tasks (project_id, task_id) VALUES (?, ?)', (project_id, task_id))
                        conn.commit()
                    else:
                        print("Task is already associated with the project.")
                else:
                    print("Task not found or doesn't belong to you.")
            else:
                print("Project not found or doesn't belong to you.")
        else:
            print("No user is currently logged in. Cannot add a task to the project.")
    
    def remove_task_from_db(self, task_id):
        """
        Function to remove specific task from database
        :param task_id: task id for specific task
        """
        # Get the list of projects associated with the task
        cursor.execute('SELECT project_id FROM project_tasks WHERE task_id = ?', (task_id,))
        projects = cursor.fetchall()

        # Remove the task from all associated projects
        for project_id in projects:
            self.remove_task_from_project(task_id, project_id[0])

        # Finally, remove the task itself
        user_id = self.user_id
        cursor.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
        conn.commit()

    def remove_task_from_project(self, task_id, project_id):
        """
        Function to remove a specific task so it is no longer associated with a project
        :param project_id: project id for specific project
        :param task_id: task id for specific task
        """
        # Remove the task from a specific project
        user_id = self.user_id
        cursor.execute('DELETE FROM project_tasks WHERE task_id = ? AND project_id = ?', (task_id, project_id))
        conn.commit()

    def get_tasks_in_project(self, project_id):
        """
        Function to access tasks associated to a project from the database
        :param project_id: project id for specific project
        """
        if self.user_id:
            # Check if the project belongs to the current user
            cursor.execute('SELECT id FROM projects WHERE id = ? AND user_id = ?', (project_id, self.user_id))
            project = cursor.fetchone()
            if project:
                # Retrieve all the task IDs associated with the project
                cursor.execute('SELECT task_id FROM project_tasks WHERE project_id = ?', (project_id,))
                task_ids = cursor.fetchall()

                # Fetch and return the details of each associated task
                associated_tasks = []
                for task_id in task_ids:
                    task_id = task_id[0]
                    task_details = list(self.get_task_details(task_id))
                    if task_details:
                        associated_tasks.append(task_details)

                return associated_tasks
            else:
                print("Project not found or doesn't belong to you.")
        else:
            print("No user is currently logged in.")
    
    def update_task(self, task_id, title, details, deadline):
        """
        Function to update the fields of a task in the database
        :param project_id: project id for specific project
        :param task_id: task id for specific task
        :param title: project title
        :param details: project details
        :param deadline: project deadline
        """
        if self.user_id:
            cursor.execute('UPDATE tasks SET title = ?, details = ?, deadline = ? WHERE id = ? AND user_id = ?', (title, details, deadline, task_id, self.user_id))
            conn.commit()

    def update_project(self, project_id, title, details, deadline):
        """
        Function to update the project of a task in the database
        :param project_id: project id for specific project
        :param title: project title
        :param details: project details
        :param deadline: project deadline
        """
        if self.user_id:
            cursor.execute('UPDATE projects SET title = ?, details = ?, deadline = ? WHERE id = ? AND user_id = ?', (title, details, deadline, project_id, self.user_id))
            conn.commit()

    def login_user(self, username, password):
        """
        Function to verify username and password to login
        :param username: user username
        :param password: user password
        :return: True if user logged in, False otherwise
        """
        cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
        user_id = cursor.fetchone()
        self.username = username
        self.password = password
        if user_id:
            self.user_id = user_id[0]
            global current_user  # Make current_user a global variable
            current_user = self  # Set the current_user to the logged-in user
            return True
        return False
    
    def logout_user(self):
        """
        Function to logout current user
        """
        global current_user
        current_user = None  # Set current_user to None on logout
        


class Data:
    """
    Class to track user data (tasks, projects, priority list)
    """

    def __init__(self):
        self.tasks = []
        self.projects = []
        self.prioritylist = []
    # def get_task(title):


class Task:
    """
    Class to manage user tasks in database
    """

    def __init__(self):
        self.title = None
        self.details = None
        self.deadline = None
        self.completed = False
        self.deleted = False
        self.users = []

    def create_task(self, title, details, deadline):
        """
        Function to create task in database
        :param title: task title
        :param details: task details
        :param deadline: task deadline
        """
        # if user is logged in
        if current_user:
            # create task
            self.title = title
            self.details = details
            self.deadline = deadline
            user_id = current_user.user_id  # Use the user ID of the currently logged-in user
            # add to database
            cursor.execute('INSERT INTO tasks (title, details, deadline, completed, deleted, user_id) VALUES (?, ?, ?, 0, 0, ?)', (self.title, self.details, self.deadline, user_id))
            conn.commit()
        else:
            print("No user is currently logged in. Cannot create a task.")

    def modify_task(self, new_title, new_details, new_deadline):
        """
        Function to modify task fields in database
        :param new_title: modified title
        :param new_details: modified details
        :param new_deadline: modified deadline
        """
        # if user logged in
        if current_user:
            # modify details
            self.title = new_title
            self.details = new_details
            self.deadline = new_deadline
            # Update the task in the database using user_id and task_id
            cursor.execute('UPDATE tasks SET title = ?, details = ?, deadline = ? WHERE id = ? AND user_id = ?', (self.title, self.details, self.deadline, self.task_id, current_user.user_id))
            conn.commit()
        else:
            print("No user is currently logged in. Cannot modify the task.")


    def complete_task(self):
        """
        Function to mark tasks as complete
        """
        self.completed = True

    def is_task_complete(self):
        """
        Function to print whether a task is completed or not
        """
        if self.completed:
            print(self.title, " is complete")
        else:
            print(self.title, " is not complete")

    def assign_task(self, *user):
        """
        Function to assign a task to a user
        """
        # multiple args - figure out later
        self.users.append(user)

    def delete_task(self):
        """
        Function to delete a task
        """
        # clear field values for task
        self.title = None
        self.details = None
        self.deadline = None
        # mark as deleted
        self.deleted = True


class Project:
    """
    Class to manage user projects
    """

    def __init__(self):
        self.title = None
        self.details = None
        self.deadline = None
        self.completed = False
        self.tasks = []
        self.users = []

    def create_project(self, title, details, deadline):
        """
        Function to create project in database
        :param title: project title
        :param details: project details
        :param deadline: project deadline
        """
        # if user is logged in
        if current_user:
            # create project
            self.title = title
            self.details = details
            self.deadline = deadline
            user_id = current_user.user_id
            # add to database
            cursor.execute('INSERT INTO projects (title, details, deadline, completed, user_id) VALUES (?, ?, ?, 0, ?)', (self.title, self.details, self.deadline, user_id))
            conn.commit()
        else:
            print("No user is currently logged in. Cannot create a project.")

    def modify_project(self, new_title, new_details):
        """
        Function to modify project in database
        :param new_title: modified project title
        :param new_details: modified project details
        """
        # if user is logged in
        if current_user:
            # modify project fields
            self.title = new_title
            self.details = new_details
            # Update the project in the database using user_id and project_id
            cursor.execute('UPDATE projects SET title = ?, details = ?, deadline = ? WHERE id = ? AND user_id = ?', (self.title, self.details, self.deadline, self.project_id, current_user.user_id))
            conn.commit()
        else:
            print("No user is currently logged in. Cannot modify the project.")

    def complete_project(self, name):
        """
        Function to mark prokject as completed
        """
        self.completed = True

    def is_project_complete(self, project_name):
        """
        Function to print whether a project is marked complete or not
        """
        if self.completed:
            print(self.title, " is complete")
        else:
            print(self.title, " is not complete")


class Dashboard:
    def __init__(self):
        self.time = datetime.datetime.now()
