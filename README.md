## Student Planner
Student Planner is a Python application that combines a monthly calendar with a to-do-list. The student planner's goal is to help students organize assignments, deadlines, and tasks by date.
## Target Users
Target users for the app are students who want a planner that locally runs on their computer.
## Features
- Browse the months using Previous and Next.
- Select a calendar date and view its tasks.
- Return to the current date with Go to Today.
- Add a task using the Add Task button or enter key.
- Mark tasks as complete or undo completion.
- Delete selected tasks.
- View the number of tasks and completed tasks for a selected date.
- Save tasks and reload them when the app opens.

## Technologies

- Python: application logic
- Tkinter: graphical interface
- calendar and datetime: calendar layout and date handling
- json: task storage
- pathlib: local file paths
- Git and GitHub: version control and code hosting

No third-party Python packages are required.

## Setup and Run

The application was developed and tested on Windows with Python 3.14.7.

1. Install Python with Tkinter support.

2. Download this repository using Code + Download ZIP and extract it,
    or clone it using Git: 
    ```powershell
    git clone https://github.com/charlisabel12-dev/To-Do-List.git
    ```
3. Open the extracted or cloned To-Do-List folder in VS Code.

4. Open a terminal in that folder.

5. Check that Tkinter is available:

    ```powershell
    python -m tkinter
    ```
    Close the demonstration window after it opens.

6. Start the application:
    ```powershell
    python app.py
    ```
If Windows does not recognize `python`, try `py` instead.

## How to Use

1. Select the date for your task.
2. Type a task title and click Add Task or press Enter.
3. Select a task in the list.
4. Click Complete / Undo to change its completion status.
5. Click Delete Task to remove it.

The app opens on today's date. To find a saved task for another date,
select that date on the calendar.

## Data Storage

Tasks are saved automatically in task. json`, beside app.py`.
The application creates this file if it does not exist.

Each task stores its title, completion status, and date.
The >.gitignore' file excludes local task data from GitHub.

Keep `task. json` to retain your tasks. To back it up, close the app
and copy the file to another folder.

## Current Limitations

- Tasks are stored locally and do not sync between devices.
- There are no reminders or recurring tasks.
- Editing a task's title or date requires deleting and recreating it.
- Deleted tasks have no undo option.
- Use one application window at a time to avoid conflicting saves.

