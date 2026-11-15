import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "task.json"


def save_tasks():
    tasks = list(task_list.get(0, tk.END))
    temporary_file = DATA_FILE.with_suffix(".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
        temporary_file.replace(DATA_FILE)
        return
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
            tasks = json.load(file)

        if not isinstance(tasks, list):
            raise ValueError("Expected a list of tasks.")

    except (OSError, ValueError) as error:

        messagebox.showerror(
            "Could not load tasks",
            f"The saved file could not be read.\n\n{error}\n\n",
            "The app will close to protect the existing file."
        )
        return False

    for task in tasks:
        task_list.insert(tk.END, task)

    return True


def add_task():
    task = task_entry.get().strip()

    if not task:
        messagebox.showwarning("Missing task", "Please enter a task.")
        return
    task_list.insert(tk.END, task)
    task_entry.delete(0, tk.END)
    save_tasks()


def toggle_complete():
    selected = task_list.curselection()

    if not selected:
        messagebox.showinfo("Select a task", "Click a task first.")
        return

    index = selected[0]
    task = task_list.get(index)

    if task.startswith("[Done] "):
        task = task.removeprefix("[Done] ")
    else:
        task = "[Done] " + task

    task_list.delete(index)
    task_list.insert(index, task)
    task_list.selection_set(index)
    save_tasks()


def delete_task():
    selected = task_list.curselection()

    if not selected:
        messagebox.showinfo("Select a task", "Click a task first.")
        return

    task_list.delete(selected[0])
    save_tasks()


window = tk.Tk()
window.title("Student Planner")
window.geometry("500x400")

heading = tk.Label(window, text="My To-Do List", font=("Arial", 20))
heading.pack(pady=15)

task_entry = tk.Entry(window, width=40)
task_entry.pack(pady=5)

add_button = tk.Button(window, text="Add Task", command=add_task)
add_button.pack(pady=5)

task_list = tk.Listbox(window, width=50, height=12)
task_list.pack(padx=20, pady=15, fill=tk.BOTH, expand=True)

button_frame = tk.Frame(window)
button_frame.pack(pady=(0, 15))

complete_button = tk.Button(
    button_frame,
    text="Complete / Undo",
    command=toggle_complete
)
complete_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(
    button_frame,
    text="Delete Task",
    command=delete_task
)
delete_button.pack(side=tk.LEFT, padx=5)

if load_tasks():
    window.mainloop()
else:
    window.destroy()
