import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from plyer import notification

# ---------- File to save tasks ----------
TASK_FILE = "tasks.json"

# ---------- Load saved tasks ----------
def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# ---------- Save tasks ----------
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# ---------- Add new task ----------
def add_task():
    task = task_entry.get()
    deadline = deadline_entry.get()

    if task == "" or deadline == "":
        messagebox.showwarning("Input Error", "Please enter both task and deadline")
        return

    try:
        # Convert deadline to datetime for validation
        datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showwarning("Format Error", "Use format YYYY-MM-DD HH:MM")
        return

    tasks.append({"task": task, "deadline": deadline, "done": False})
    save_tasks(tasks)
    update_task_list()
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)

# ---------- Mark selected task as done ----------
def mark_done():
    selected = task_list.curselection()
    if not selected:
        messagebox.showinfo("No Selection", "Select a task to mark as done")
        return

    index = selected[0]
    tasks[index]["done"] = True
    save_tasks(tasks)
    update_task_list()

# ---------- Update task display ----------
def update_task_list():
    task_list.delete(0, tk.END)
    for i, t in enumerate(tasks):
        status = "✓" if t["done"] else "✗"
        task_list.insert(tk.END, f"{i+1}. {t['task']} | Deadline: {t['deadline']} | Status: {status}")

# ---------- Check deadlines for notifications ----------
def check_deadlines():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for t in tasks:
        if not t["done"] and t["deadline"] == now:
            notification.notify(
                title="⏰ Task Reminder",
                message=f"Task: {t['task']} is due now!",
                timeout=10
            )
    root.after(60000, check_deadlines)  # check every 1 min

# ---------- GUI Setup ----------
root = tk.Tk()
root.title(" Time Management Software ")
root.geometry("600x400")

tasks = load_tasks()

# Input fields
tk.Label(root, text="Task:").pack()
task_entry = tk.Entry(root, width=50)
task_entry.pack()

tk.Label(root, text="Deadline (YYYY-MM-DD HH:MM):").pack()
deadline_entry = tk.Entry(root, width=50)
deadline_entry.pack()

# Buttons
tk.Button(root, text="Add Task", command=add_task).pack(pady=5)
tk.Button(root, text="Mark as Done", command=mark_done).pack(pady=5)

# Task List
task_list = tk.Listbox(root, width=80, height=10)
task_list.pack(pady=10)

# Initialize
update_task_list()
check_deadlines()

root.mainloop()
