import calendar
import json
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import messagebox

DATA_FILE = Path(__file__).resolve().parent / "task.json"

tasks = []

visible_indices = []

selected_date = date.today()

displayed_month = selected_date.replace(day=1)


def save_tasks():
    temporary_file = DATA_FILE.with_suffix(".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)

        temporary_file.replace(DATA_FILE)
        return True

    except OSError as error:
        messagebox.showerror(
            "Could not save",
            f"Your latest changes were not saved.\n\n{error}"
        )
        return False


def load_tasks():
    if not DATA_FILE.exists():
        return True

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            saved_tasks = json.load(file)

        if not isinstance(saved_tasks, list):
            raise ValueError("Expected a list of tasks.")

        converted_tasks = []

        for item in saved_tasks:
            if isinstance(item, str):
                item = {
                    "title": item.removeprefix("[Done] "),
                    "done": item.startswith("[Done] "),
                    "date": date.today().isoformat()
                }

            if not isinstance(item, dict):
                raise ValueError("Invalid task record.")

            if not isinstance(item.get("title"), str):
                raise ValueError("A task must be a text.")

            if not isinstance(item.get("done"), bool):
                raise ValueError("A task must have a completion status.")

            if not isinstance(item.get("date"), str):
                raise ValueError("A task must have a date.")

            task_date = date.fromisoformat(item["date"])

            converted_tasks.append({
                "title": item["title"],
                "done": item["done"],
                "date": task_date.isoformat()
            })

        tasks.extend(converted_tasks)
        return True

    except (OSError, ValueError) as error:
        messagebox.showerror(
            "Could not load tasks",
            f"The saved file could not be read.\n\n{error}\n\n"
            "The app will close to protect the existing file."
        )
        return False


def refresh_tasks():
    task_list.delete(0, tk.END)
    visible_indices.clear()

    date_label.config(
        text=f"Tasks for {selected_date.strftime('%B %d, %Y')}"
    )

    completed = 0

    for index, task in enumerate(tasks):
        if task["date"] == selected_date.isoformat():
            visible_indices.append(index)

            prefix = "[Done] " if task["done"] else "[To do] "
            task_list.insert(tk.END, prefix + task["title"]
                             )
            if task["done"]:
                completed += 1

    total = len(visible_indices)
    status_label.config(
        text=f"{total} task(s) - {completed} completed"
    )


def add_task():

    title = task_entry.get().strip()

    if not title:

        messagebox. showwarning("Missing task", "Please enter a task.")
        return

    tasks. append({
        "title": title,
        "done": False,
        "date": selected_date.isoformat()
    })

    if not save_tasks():

        tasks.pop()

        return

    task_entry.delete(0, tk.END)
    refresh_tasks()
    task_entry.focus_set()


def get_selected_task_index():

    selected = task_list.curselection()

    if not selected:

        messagebox. showinfo("Select a task", "Click a task first.")
        return None

    row = selected[0]
    return visible_indices[row]


def toggle_complete():

    index = get_selected_task_index()

    if index is None:

        return

    row = task_list.curselection()[0]
    tasks[index]["done"] = not tasks[index]["done"]

    if not save_tasks():
        tasks[index]["done"] = not tasks[index]["done"]
        return

    refresh_tasks()
    task_list.selection_set(row)


def delete_task():

    index = get_selected_task_index()

    if index is None:

        return

    removed_task = tasks. pop(index)

    if not save_tasks():
        tasks. insert(index, removed_task)
        return

    refresh_tasks()


def select_day(day):

    global selected_date

    selected_date = date(
        displayed_month.year,
        displayed_month.month,
        day
    )

    draw_calendar()
    refresh_tasks()


def change_month(direction):

    global displayed_month

    month_number = (
        displayed_month.year * 12
        + displayed_month.month - 1
        + direction
    )
    year, month_index = divmod(month_number, 12)

    if 1 <= year <= 9999:
        displayed_month = date(year, month_index + 1, 1)
        select_day(1)


def go_to_today():

    global displayed_month

    today = date. today()
    displayed_month = today.replace(day=1)
    select_day(today.day)


def draw_calendar():

    for widget in calendar_frame.winfo_children():
        widget.destroy()

    month_label.config(
        text=displayed_month.strftime("%B %Y")
    )

    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for column, weekday in enumerate(weekdays):
        tk. Label(

            calendar_frame,

            text=weekday,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=column, padx=3, pady=5)

    weeks = calendar.Calendar(firstweekday=0).monthdayscalendar(
        displayed_month.year,
        displayed_month.month
    )

    for row, week in enumerate(weeks, start=1):

        for column, day in enumerate(week):

            if day == 0:
                continue

            button = tk.Button(
                calendar_frame,
                text=str(day),
                width=4,
                command=lambda d=day: select_day(d)
            )

            button.grid(
                row=row,
                column=column,
                padx=3,
                pady=3,
                sticky="ew"
            )

            if day == selected_date.day:
                button.config(
                    bg="#2457A7",
                    fg="white",
                    relief=tk.SUNKEN
                )

    for column in range(7):
        calendar_frame.columnconfigure(column, weight=1)


window = tk.Tk()
window.title("Student Planner")
window.geometry("650x720")
window.minsize(560, 680)

heading = tk.Label(
    window,
    text="Student Planner",
    font=("Arial", 22, "bold")
)

heading.pack(pady=(15, 10))

navigation_frame = tk.Frame(window)
navigation_frame.pack(fill=tk.X, padx=25)

tk.Button(
    navigation_frame,
    text="< Previous",
    command=lambda: change_month(-1)
).pack(side=tk. LEFT)

tk.Button(
    navigation_frame,
    text="Next >",
    command=lambda: change_month(1)
).pack(side=tk.RIGHT)

month_label = tk. Label(
    navigation_frame,
    font=("Arial", 14, "bold")
)
month_label.pack()

calendar_frame = tk.Frame(window)
calendar_frame.pack(fill=tk.X, padx=25, pady=8)

tk.Button(
    window,
    text="Go to Today",
    command=go_to_today
).pack(pady=(0, 8))

date_label = tk.Label(window, font=("Arial", 13, "bold"))
date_label.pack(pady=5)

entry_frame = tk.Frame(window)
entry_frame.pack(fill=tk.X, padx=25, pady=5)

task_entry = tk.Entry(entry_frame, font=("Arial", 11))
task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
task_entry.bind("<Return>", lambda event: add_task())

tk.Button(
    entry_frame,
    text="Add Task",
    command=add_task
).pack(side=tk.RIGHT)

list_frame = tk.Frame(window)
list_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_list = tk.Listbox(
    list_frame,
    font=("Arial", 11),
    height=8,
    exportselection=False,
    yscrollcommand=scrollbar.set
)
task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=task_list.yview)

status_label = tk.Label(window)
status_label.pack()

button_frame = tk.Frame(window)
button_frame.pack(pady=12)
tk.Button(
    button_frame,
    text="Complete / Undo",
    command=toggle_complete
).pack(side=tk. LEFT, padx=5)

tk.Button(
    button_frame,
    text="Delete Task",
    command=delete_task
).pack(side=tk.LEFT, padx=5)

if load_tasks():

    if save_tasks():
        draw_calendar()
        refresh_tasks()
        window.mainloop()

    else:
        window.destroy()

else:
    window.destroy()
