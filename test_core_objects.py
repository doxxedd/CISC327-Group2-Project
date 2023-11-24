import datetime
import sqlite3
from shared import user
"""Backend classes to be used in next iterations of the prototype
    """
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
current_user = None


class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.data = Data()
        self.user_id = None

    def save_user(self):
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (self.username, self.password))
        conn.commit()

    def get_user_tasks(self):
        tasks = []
        if self.user_id:
            cursor.execute('SELECT id, title FROM tasks WHERE user_id = ? AND deleted = 0', (self.user_id,))
            tasks = cursor.fetchall()
        return tasks

    def get_user_projects(self):
        if self.user_id:
            cursor.execute('SELECT id, title FROM projects WHERE user_id = ?', (self.user_id,))
            tasks = cursor.fetchall()
        return tasks

    def get_task_details(self, task_id):
        task_details = None
        if self.user_id:
            cursor.execute('SELECT id, title, details, deadline FROM tasks WHERE id = ? AND user_id = ? AND deleted = 0', (task_id, self.user_id))
            task_details = cursor.fetchone()
        return task_details

    def get_project_details(self, project_id):
        project_details = None
        if self.user_id:
            cursor.execute('SELECT id, title, details, deadline FROM projects WHERE id = ? AND user_id = ?', (project_id, self.user_id))
            project_details = cursor.fetchone()
        return project_details

    def add_task_to_project(self, project_id, task_id):
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
        # Remove the task from a specific project
        user_id = self.user_id
        cursor.execute('DELETE FROM project_tasks WHERE task_id = ? AND project_id = ?', (task_id, project_id))
        conn.commit()

    def remove_project(self, project_id):
        if self.user_id:
            # First, check if the project exists and belongs to the user
            cursor.execute('SELECT id FROM projects WHERE id = ? AND user_id = ?', (project_id, self.user_id))
            project = cursor.fetchone()
            if project:
                # Remove all task associations with the project
                cursor.execute('DELETE FROM project_tasks WHERE project_id = ?', (project_id,))

                # Remove the project itself
                cursor.execute('DELETE FROM projects WHERE id = ? AND user_id = ?', (project_id, self.user_id))
                conn.commit()
                return True
            else:
                print("Project not found or doesn't belong to you.")
        else:
            print("No user is currently logged in. Cannot remove a project.")
        return False

    # def get_tasks_in_project(self, project_id):
    #     if self.user_id:
    #         # Check if the project belongs to the current user
    #         cursor.execute('SELECT id FROM projects WHERE id = ? AND user_id = ?', (project_id, self.user_id))
    #         project = cursor.fetchone()
    #         if project:
    #             # Retrieve all the task IDs associated with the project
    #             cursor.execute('SELECT task_id FROM project_tasks WHERE project_id = ?', (project_id,))
    #             task_ids = cursor.fetchall()

    #             # Fetch and return the details of each associated task
    #             associated_tasks = []
    #             for task_id in task_ids:
    #                 task_id = task_id[0]
    #                 task_details = list(self.get_task_details(task_id))
    #                 if task_details:
    #                     associated_tasks.append(task_details)

    #             return associated_tasks
    #         else:
    #             print("Project not found or doesn't belong to you.")
    #     else:
    #         print("No user is currently logged in.")
    #         return None
        
    def get_tasks_in_project_mutant1(self, project_id):
        if not self.user_id:
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
            return None
        
    def get_tasks_in_project_mutant2(self, project_id):
        if self.user_id:
            # Check if the project belongs to the current user
            cursor.execute('SELECT id FROM projects WHERE id = ? AND user_id = ?', (project_id, self.user_id))
            project = cursor.fetchone()
            if not project:
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
            return None
    
    def get_tasks_in_project_mutant3(self, project_id):
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
                    task_id = task_id[1]
                    task_details = list(self.get_task_details(task_id))
                    if task_details:
                        associated_tasks.append(task_details)

                return associated_tasks
            else:
                print("Project not found or doesn't belong to you.")
        else:
            print("No user is currently logged in.")
            return None
        
    def get_tasks_in_project_mutant4(self, project_id):
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
                    if not task_details:
                        associated_tasks.append(task_details)

                return associated_tasks
            else:
                print("Project not found or doesn't belong to you.")
        else:
            print("No user is currently logged in.")
            return None
        
    def get_tasks_in_project_mutant5(self, project_id):
        if self.user_id:
            # Check if the project belongs to the current user
            cursor.execute('SELECT id FROM projects WHERE id = ? AND user_id = ?', (project_id, self.user_id))
            project = cursor.fetchone()
            if project:
                # Retrieve all the task IDs associated with the project
                cursor.execute('SELECT task_id FROM project_tasks WHERE project_id = ?', (project_id,))
                task_ids = cursor.fetchall()

                # Fetch and return the details of each associated task
                # associated_tasks = []
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
            return None

    def update_task(self, task_id, title, details, deadline):
        if self.user_id:
            cursor.execute('UPDATE tasks SET title = ?, details = ?, deadline = ? WHERE id = ? AND user_id = ?', (title, details, deadline, task_id, self.user_id))
            conn.commit()

    def update_project(self, project_id, title, details, deadline):
        if self.user_id:
            cursor.execute('UPDATE projects SET title = ?, details = ?, deadline = ? WHERE id = ? AND user_id = ?', (title, details, deadline, project_id, self.user_id))
            conn.commit()

    def login_user(self, username, password):
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
        global current_user
        current_user = None  # Set current_user to None on logout


class Data:
    def __init__(self):
        self.tasks = []
        self.projects = []
        self.prioritylist = []
    # def get_task(title):


class Task:

    def __init__(self):
        self.title = None
        self.details = None
        self.deadline = None
        self.completed = False
        self.deleted = False
        self.users = []

    def create_task(self, title, details, deadline):
        if current_user:
            self.title = title
            self.details = details
            self.deadline = deadline
            user_id = current_user.user_id  # Use the user ID of the currently logged-in user
            cursor.execute('INSERT INTO tasks (title, details, deadline, completed, deleted, user_id) VALUES (?, ?, ?, 0, 0, ?)', (self.title, self.details, self.deadline, user_id))
            conn.commit()
        else:
            print("No user is currently logged in. Cannot create a task.")

    def modify_task(self, new_title, new_details, new_deadline):
        if current_user:
            self.title = new_title
            self.details = new_details
            self.deadline = new_deadline
            # Update the task in the database using user_id and task_id
            cursor.execute('UPDATE tasks SET title = ?, details = ?, deadline = ? WHERE id = ? AND user_id = ?', (self.title, self.details, self.deadline, self.task_id, current_user.user_id))
            conn.commit()
        else:
            print("No user is currently logged in. Cannot modify the task.")

    def complete_task(self):
        self.completed = True

    def is_task_complete(self):
        if self.completed:
            print(self.title, " is complete")
        else:
            print(self.title, " is not complete")

    def assign_task(self, *user):
        # multiple args - figure out later
        self.users.append(user)

    def delete_task(self):
        self.title = None
        self.details = None
        self.deadline = None
        self.deleted = True


class Project:
    def __init__(self):
        self.title = None
        self.details = None
        self.deadline = None
        self.completed = False
        self.tasks = []
        self.users = []

    def create_project(self, title, details, deadline):
        if current_user:
            self.title = title
            self.details = details
            self.deadline = deadline
            user_id = current_user.user_id
            cursor.execute('INSERT INTO projects (title, details, deadline, completed, user_id) VALUES (?, ?, ?, 0, ?)', (self.title, self.details, self.deadline, user_id))
            conn.commit()
        else:
            print("No user is currently logged in. Cannot create a project.")

    def modify_project(self, new_title, new_details):

        if current_user:
            self.title = new_title
            self.details = new_details
            # Update the project in the database using user_id and project_id
            cursor.execute('UPDATE projects SET title = ?, details = ?, deadline = ? WHERE id = ? AND user_id = ?', (self.title, self.details, self.deadline, self.project_id, current_user.user_id))
            conn.commit()
        else:
            print("No user is currently logged in. Cannot modify the project.")

    def complete_project(self):
        self.completed = True

    def is_project_complete(self):
        if self.completed:
            print(self.title, " is complete")
        else:
            print(self.title, " is not complete")


class Dashboard:
    def __init__(self):
        self.time = datetime.datetime.now()
