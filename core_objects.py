import datetime

import sqlite3
from shared import user
"""Backend classes to be used in next iterations of the prototype
    """
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
current_user = None

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

class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.data = Data()

    def save_user(self):
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (self.username, self.password))
        conn.commit()

    def get_user_tasks(self):
        tasks = []
        if self.user_id:
            cursor.execute('SELECT id, title FROM tasks WHERE user_id = ? AND deleted = 0', (self.user_id,))
            tasks = cursor.fetchall()
        return tasks
    
    def get_task_details(self, task_id):
        task_details = None
        if self.user_id:
            cursor.execute('SELECT id, title, details, deadline FROM tasks WHERE id = ? AND user_id = ? AND deleted = 0', (task_id, self.user_id))
            task_details = cursor.fetchone()
        return task_details
    
    def remove_task_from_db(self, task_id):
        # Remove the task from the database based on its ID
        user_id = self.user_id  # Get the current user's ID
        cursor.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
        conn.commit()
    
    def update_task(self, task_id, title, details, deadline):
        if self.user_id:
            cursor.execute('UPDATE tasks SET title = ?, details = ?, deadline = ? WHERE id = ? AND user_id = ?', (title, details, deadline, task_id, self.user_id))
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

    def complete_project(self, name):
        self.completed = True

    def is_project_complete(self, project_name):
        if self.completed:
            print(self.title, " is complete")
        else:
            print(self.title, " is not complete")


class Dashboard:
    def __init__(self):
        self.time = datetime.datetime.now()
