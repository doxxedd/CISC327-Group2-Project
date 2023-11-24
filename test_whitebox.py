import shared
import landingpage
import test_core_objects 
import core_objects
import sqlite3
import pytest
import sys

# mutation testing for get project details
def test_get_project_details_correct():
    user = core_objects.User()
    user.login_user("test", "test")
    
    tasks = user.get_tasks_in_project(1)

    assert tasks == [[1, 'one', 'one', '2023-11-23'], [2, 'two', 'two', '2023-11-23'], [3, 'three', 'three', '2023-11-23']]

def test_get_project_details_mutant1():
    # first if statement mutant
    user = test_core_objects.User()
    user.login_user("test", "test")
    
    tasks = user.get_tasks_in_project_mutant1(1)

    assert tasks == [[1, 'one', 'one', '2023-11-23'], [2, 'two', 'two', '2023-11-23'], [3, 'three', 'three', '2023-11-23']]

def test_get_project_details_mutant2():
    # second if statement mutant
    user = test_core_objects.User()
    user.login_user("test", "test")
    
    tasks = user.get_tasks_in_project_mutant2(1)

    assert tasks == [[1, 'one', 'one', '2023-11-23'], [2, 'two', 'two', '2023-11-23'], [3, 'three', 'three', '2023-11-23']]

def test_get_project_details_mutant3():
    # change task id index mutant
    user = test_core_objects.User()
    user.login_user("test", "test")
    
    tasks = user.get_tasks_in_project_mutant3(1)

    assert tasks == [[1, 'one', 'one', '2023-11-23'], [2, 'two', 'two', '2023-11-23'], [3, 'three', 'three', '2023-11-23']]

def test_get_project_details_mutant4():
    # third if statement mutant
    user = test_core_objects.User()
    user.login_user("test", "test")
    
    tasks = user.get_tasks_in_project_mutant4(1)

    assert tasks == [[1, 'one', 'one', '2023-11-23'], [2, 'two', 'two', '2023-11-23'], [3, 'three', 'three', '2023-11-23']]

def test_get_project_details_mutant5():
    # remove associated_tasks list initializer line mutant
    user = test_core_objects.User()
    user.login_user("test", "test")
    
    tasks = user.get_tasks_in_project_mutant5(1)

    assert tasks == [[1, 'one', 'one', '2023-11-23'], [2, 'two', 'two', '2023-11-23'], [3, 'three', 'three', '2023-11-23']]


def test_add_task_to_project_path1(capsys):
    # original accepted path
    user = core_objects.User()
    user.login_user("test", "test")
    user.add_task_to_project(1, 10)
    user.remove_task_from_project(10, 1)
    captured = capsys.readouterr()
    assert captured == ('', '')
   
    
def test_add_task_to_project_path2(capsys):
    # first independent path mutant - task already in project
    user = core_objects.User()
    user.login_user("test", "test")
    user.add_task_to_project(1, 10)
    user.add_task_to_project(1, 10)
    user.remove_task_from_project(10, 1)
    user.remove_task_from_project(10, 1)
    captured = capsys.readouterr()
    assert captured == ('Task is already associated with the project.\n', '')

def test_add_task_to_project_path3(capsys):
    # second independent path mutant - task does not exist
    user = core_objects.User()
    user.login_user("test", "test")
    user.add_task_to_project(1, 20)
    captured = capsys.readouterr()
    assert captured == ('Task not found or doesn\'t belong to you.\n', '')

def test_add_task_to_project_path4(capsys):
    # third independent path mutant - project does not exist
    user = core_objects.User()
    user.login_user("test", "test")
    user.add_task_to_project(2, 1)
    captured = capsys.readouterr()
    assert captured == ('Project not found or doesn\'t belong to you.\n', '')

def test_add_task_to_project_path5(capsys):
    # fourth independent path mutant - no user logged in
    user = core_objects.User()
    user.add_task_to_project(2, 1)
    captured = capsys.readouterr()
    assert captured == ('No user is currently logged in. Cannot add a task to the project.\n', '')
   
    






   
    

       



if __name__ == "__main__":
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            task_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')

    conn.commit()
    conn.close()
    pytest 
    # test_add_task_to_project_path1()
    # test_get_project_details()