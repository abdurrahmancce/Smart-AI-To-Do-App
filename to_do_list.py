import tkinter as tk
from tkinter import messagebox
import datetime

try:
    import matplotlib.pyplot as plt  # pyright: ignore[reportMissingModuleSource]
    HAS_MATPLOTLIB = True
except ImportError:
    plt = None
    HAS_MATPLOTLIB = False

FILE_NAME = "tasks.txt"

# ----------------------------
# Smart AI Logic
# ----------------------------
def auto_priority(task):
    task = task.lower()
    if any(word in task for word in ["exam", "deadline", "urgent"]):
        return "High"
    elif any(word in task for word in ["study", "project"]):
        return "Medium"
    return "Low"

# ----------------------------
# Save / Load
# ----------------------------
def load_tasks():
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                task_list.insert(tk.END, line.strip())
    except FileNotFoundError:
        pass

def save_tasks():
    with open(FILE_NAME, "w") as f:
        for task in task_list.get(0, tk.END):
            f.write(task + "\n")

# ----------------------------
# Animation (Flash)
# ----------------------------
def flash_widget(widget, color1, color2, count=4):
    def animate(c):
        if c <= 0:
            widget.config(bg=color2)
            return
        widget.config(bg=color1 if c % 2 == 0 else color2)
        root.after(100, animate, c-1)
    animate(count)

# ----------------------------
# Animated Background
# ----------------------------
colors = ["#1e1e2f", "#2c3e50", "#34495e", "#2c3e50"]

def animate_bg(i=0):
    root.config(bg=colors[i])
    root.after(1500, animate_bg, (i+1) % len(colors))

# ----------------------------
# Add Task
# ----------------------------
def add_task():
    task = entry_task.get().strip()
    date = entry_date.get().strip()
    time = entry_time.get().strip()
    category = category_var.get()

    if not task:
        messagebox.showwarning("Warning", "Task cannot be empty!")
        return

    priority = auto_priority(task)

    full_task = f"{task} | {date} {time} | {priority} | {category}"
    task_list.insert(tk.END, full_task)

    entry_task.delete(0, tk.END)
    save_tasks()
    flash_widget(task_list, "#00ffcc", "white")

# ----------------------------
# Delete Task
# ----------------------------
def delete_task():
    try:
        index = task_list.curselection()[0]
        task_list.delete(index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task!")

# ----------------------------
# Mark Done
# ----------------------------
def mark_done():
    try:
        index = task_list.curselection()[0]
        task = task_list.get(index)
        task_list.delete(index)
        task_list.insert(index, "✔️ " + task)
        save_tasks()
        flash_widget(task_list, "#66ccff", "white")
    except IndexError:
        messagebox.showwarning("Warning", "Select a task!")

# ----------------------------
# Dashboard (Chart)
# ----------------------------
def show_dashboard():
    tasks = task_list.get(0, tk.END)

    total = len(tasks)
    done = sum(1 for t in tasks if "✔️" in t)
    pending = total - done

    if not HAS_MATPLOTLIB:
        messagebox.showinfo(
            "Dashboard",
            f"Total: {total}\nDone: {done}\nPending: {pending}\n\nInstall matplotlib to see charts."
        )
        return

    plt.figure()
    plt.pie([done, pending], labels=["Done", "Pending"], autopct='%1.1f%%')
    plt.title("Task Progress")
    plt.show()

# ----------------------------
# Dark Mode
# ----------------------------
dark_mode = False

def toggle_dark():
    global dark_mode
    dark_mode = not dark_mode

    bg = "#121212" if dark_mode else "white"
    fg = "white" if dark_mode else "black"

    root.config(bg=bg)
    for widget in root.winfo_children():
        try:
            widget.config(bg=bg, fg=fg)
        except:
            pass

# ----------------------------
# Reminder System
# ----------------------------
def check_reminder():
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

    for task in task_list.get(0, tk.END):
        if now in task:
            messagebox.showinfo("Reminder", f"Task Due:\n{task}")

    root.after(60000, check_reminder)

# ----------------------------
# Hover Effect
# ----------------------------
def on_enter(e):
    e.widget.config(bg="#ff4d4d")

def on_leave(e):
    e.widget.config(bg="SystemButtonFace")

# ----------------------------
# UI Setup
# ----------------------------
root = tk.Tk()
root.title("Smart AI To-Do App")
root.geometry("420x600")

tk.Label(root, text="🧠 Smart To-Do App", font=("Arial", 16)).pack(pady=10)

entry_task = tk.Entry(root)
entry_task.pack(pady=5)

entry_date = tk.Entry(root)
entry_date.insert(0, "DD-MM-YYYY")
entry_date.pack()

entry_time = tk.Entry(root)
entry_time.insert(0, "HH:MM")
entry_time.pack()

category_var = tk.StringVar(value="Work")
tk.OptionMenu(root, category_var, "Work", "Study", "Personal").pack(pady=5)

buttons = [
    ("Add Task", add_task),
    ("✔ Mark Done", mark_done),
    ("❌ Delete", delete_task),
    ("📊 Dashboard", show_dashboard),
    ("🌙 Dark Mode", toggle_dark)
]

for text, cmd in buttons:
    btn = tk.Button(root, text=text, command=cmd)
    btn.pack(pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

task_list = tk.Listbox(root)
task_list.pack(expand=True, fill="both", pady=10)

# Start
load_tasks()
check_reminder()
animate_bg()

root.mainloop()