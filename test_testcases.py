import pytest
from unittest.mock import patch
from io import StringIO
from core_objects import Task, current_user
from shared import user
import landingpage
import dashboard
import sqlite3
import curses
import shared
import test_auto_interaction

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
# current_user = User()  # Initialize current_user as an instance of the User class

def test_login():

    result = shared.dict["login"]
    # Check the output to verify the expected message
   
    assert result is True

def test_wrong_login():
    

    result = landingpage.validate_user("unkown", "test")
    # Check the output to verify the expected message
   
    assert result is True

def test_create_task():
    

    result = shared.dict["create_task"]
    # Check the output to verify the expected message
   
    assert result == "Task Created Succesfully"

def test_create_project():

    result = shared.dict["create_project"]
    # Check the output to verify the expected message
   
    assert result == "Project Created Succesfully"


def test_modify_project():

    result = shared.dict["create_project"]
    # Check the output to verify the expected message
   
    assert result == "Project Created Succesfully"

def test_modify_task():

    result = shared.dict["modify_task"]
    # Check the output to verify the expected message
   
    assert result == "Task Modified Successfully"

def test_modify_project():

    result = shared.dict["modify_project"]
    # Check the output to verify the expected message
   
    assert result == "Project Title Modified successfully, Task Added to Project Successfully"

def test_remove_task():

    result = shared.dict["remove_task"]
    # Check the output to verify the expected message
   
    assert result == "Task Deleted Successfully"

def test_remove_project():

    result = shared.dict["remove_project"]
    # Check the output to verify the expected message
   
    assert result == "Project Deleted Successfully"

def test_view_task():

    result = shared.dict["view_task"]
    # Check the output to verify the expected message
   
    assert result == "Tasks Viewed Successfully"

def test_view_project():

    result = shared.dict["view_project"]
    # Check the output to verify the expected message
   
    assert result == "Project Viewed Successfully"


if __name__ == "__main__":
    test_auto_interaction.main()
    pytest.main()
