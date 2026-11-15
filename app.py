import tkinter as tk
from tkinter import messagebox


def add_task():
    task = task_entry.get().strip()

    if not task:
        messagebox.showwarning("Missing task", "Please enter a task.")
        return
    task_list.insert(tk.END, task)
    task_entry.delete(0, tk.END)


def toggle_complete():
    selected = task_list.curselection()

    if not selected:
        messagebox("Select a task", "Click a task first")
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


def delete_task():
    selected = task_list.curselection()

    if not selected:
        messagebox.showinfo("Select a task", "Click a task first.")
        return

    task_list.delete(selected[0])


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

window.mainloop()
