import datetime


class User:
    def __init__(self):
        self.username = None
        self.password = None
        self.data = Data()

    def login_user(self, username, password):
        pass


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
        self.title = title
        self.details = details
        self.deadline = deadline
        current_user.data.tasks.append(self)

    def modify_task(self, new_title, new_details, new_deadline):
        self.title = new_title
        self.details = new_details
        self.deadline = new_deadline

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
        self.completed = False
        self.tasks = []
        self.users = []

    def create_project(self, title, details):
        self.title = title
        self.details = details

    def modify_project(self, new_title, new_details, new_deadline):
        self.title = new_title
        self.details = new_details
        self.deadline = new_deadline

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
