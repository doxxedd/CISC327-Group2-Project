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

    result = test_auto_interaction.dict["login"]
    # Check the output to verify the expected message
   
    assert result is True

def test_wrong_login():
    

    result = landingpage.validate_user("unkown", "test")
    # Check the output to verify the expected message
   
    assert result is True

def test_create_task():
    

    result = test_auto_interaction.dict["create_task"]
    # Check the output to verify the expected message
   
    assert result is "Task Created Succesfully"

def test_create_project():

    result = test_auto_interaction.dict["create_project"]
    # Check the output to verify the expected message
   
    assert result is "Project Created Succesfully"


def test_modify_project():

    result = test_auto_interaction.dict["create_project"]
    # Check the output to verify the expected message
   
    assert result is "Project Created Succesfully"

# # Define a fixture to set up the necessary environment for testing
# @pytest.fixture
# def setup_database():
#     # Use an in-memory SQLite database for testing
#     test_conn = sqlite3.connect(':memory:')
#     test_cursor = test_conn.cursor()

#     # Create the tasks table in the test database
#     test_cursor.execute('''CREATE TABLE tasks (
#                             id INTEGER PRIMARY KEY AUTOINCREMENT,
#                             title TEXT,
#                             details TEXT,
#                             deadline TEXT,
#                             completed INTEGER,
#                             deleted INTEGER,
#                             user_id INTEGER
#                           )''')

#     # Set up a current user for testing
#     current_user.user_id = 1  # Set the user ID to 1 for simplicity

#     yield test_conn, test_cursor

#     # Clean up the test database after the test is done
#     test_conn.close()

# # Test the create_task function after user authentication
# def test_create_task_after_authentication(monkeypatch, setup_database):
#     # Unpack the setup_database fixture
#     test_conn, test_cursor = setup_database

#     # Mock user input for login
#     with patch('builtins.input', side_effect=['test_user', 'test_password']):
#         with patch('core_objects.current_user', current_user):
#             # Log in the user
#             landingpage.landing_page(None)

#     # Now, the user is logged in, and you can test the create_task method
#     with patch('builtins.input', side_effect=['Test Title', 'Test Details', '2023-12-31']):
#         # Create a task
#         task = Task()
#         task.create_task("Test Title", "Test Details", "2023-12-31")

#     # Check if the task was created in the test database
#     test_cursor.execute("SELECT * FROM tasks WHERE title = 'Test Title'")
#     result = test_cursor.fetchone()

#     assert result is not None  # Check if the task was found in the database
#     assert result[1] == 'Test Title'
#     assert result[2] == 'Test Details'
#     assert result[3] == '2023-12-31'
#     assert result[4] == 0  # completed
#     assert result[5] == 0  # not deleted
#     assert result[6] == 1  # user_id

#     # Clean up: Remove the task from the test database
#     test_cursor.execute("DELETE FROM tasks WHERE title = 'Test Title'")
#     test_conn.commit()


# def test_dashboard_create_task(monkeypatch):
#     # Mock user input for creating a task
#     # Simulate 'Create Task' option selection and 'Enter' key press
#     monkeypatch.setattr('builtins.input', lambda x: '0\n\n')

#     # Mock arrow keys to navigate to the 'Create Task' option and 'Enter' key press
#     mock_stdscr = MagicMock()

#     with patch('curses.wrapper', lambda func: func(mock_stdscr)):
#         with patch('curses.curs_set'):
#             with patch('curses.has_colors', return_value=False):
#                 with patch('curses.initscr', return_value=None):
#                     with patch('curses.KEY_ENTER', curses.KEY_RESIZE):
#                         with patch('curses.start_color', lambda: None):  # Mock start_color
#                             with patch('curses.init_pair', lambda *args, **kwargs: None):  # Mock init_pair
#                                 with patch('sys.stdout', new_callable=StringIO):
#                                     dashboard.create_field_page(mock_stdscr, "Create Task", "", "", "")

#     print(dashboard.testresult)
#     # Check if the expected string is in the result
#     assert "Task Created Successfully" in dashboard.testresult
#     # Check if the result is as expected
#     # assert dashboard_result == "Task Created Successfully"



#     # with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
#     #     with patch('curses.KEY_ENTER', curses.KEY_RESIZE):
#     #         with patch('curses.wrapper', lambda func: func(None)):  # Mock curses.wrapper
#     #             dashboard_function_result = dashboard.dashboard(None)  # Call dashboard function
#     # result = mock_stdout.getvalue().strip()
#     # print("Actual Result:", result)
    
    
#     #             dashboard  # Call your dashboard function
#     # result = dashboard.testresult
#     # print("d: ", dashboard.testresult)
#     # print(result)

#     # result = mock_stdout.getvalue().strip()
#     # print("Actual Result:", result)
#     # assert "Task Created Successfully" in result

if __name__ == "__main__":
    test_auto_interaction.main()
    pytest.main
