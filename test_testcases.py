import pytest
from unittest.mock import patch
from io import StringIO
import dashboard
import landingpage
import curses




def test_login(monkeypatch):
    # Mock the user input to simulate different scenarios
    inputs = ['test', '\n', 'test', '\n']

    result = landingpage.validate_user("test", "test")
    # Check the output to verify the expected message
   
    assert result is True

def test_wrong_login(monkeypatch):
    # Mock the user input to simulate different scenarios
    inputs = ['test', '\n', 'test', '\n']

    result = landingpage.validate_user("unkown", "test")
    # Check the output to verify the expected message
   
    assert result is True

def test_dashboard_create_task(monkeypatch):
    # Mock user input for creating a task
    # Simulate 'Create Task' option selection and 'Enter' key press
    monkeypatch.setattr('builtins.input', lambda x: '0\n\n')

    # Mock arrow keys to navigate to the 'Create Task' option and 'Enter' key press
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        with patch('curses.KEY_ENTER', curses.KEY_RESIZE):
            with patch('curses.wrapper', lambda func: func(None)):  # Mock curses.wrapper
                dashboard  # Call your dashboard function
    result = dashboard.testresult

    # result = mock_stdout.getvalue().strip()
    print("Actual Result:", result)
    assert "Task Created Successfully" in result