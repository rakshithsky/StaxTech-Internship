import tkinter as tk
from tkinter import messagebox
import json, os
from datetime import datetime

FILE_NAME = "tasks.json"

# ---------- FUNCTIONS ----------
def load_tasks():
    """Load tasks from JSON memory (supports old and new formats)"""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            try:
                data = json.load(f)
                # Old format: list of plain strings
                if isinstance(data, list) and all(isinstance(x, str) for x in data):
                    for task in data:
                        add_task_ui(task, datetime.now().strftime("%d %b %Y • %I:%M %p"), False)
                # New format: list of dicts
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            add_task_ui(item.get("task", ""), item.get("time", ""), item.get("done", False))
            except json.JSONDecodeError:
                pass

def save_tasks():
    """Save all tasks (with time & done state)"""
    all_tasks = []
    for widget in tasks_frame.winfo_children():
        task_label = widget.winfo_children()[1]
        time_label = widget.winfo_children()[2]
        done = getattr(widget, "done", False)
        all_tasks.append({
            "task": task_label.cget("text").replace("✅ ", ""),
            "time": time_label.cget("text"),
            "done": done
        })
    with open(FILE_NAME, "w") as f:
        json.dump(all_tasks, f, indent=2)

def add_task():
    """Add new task with current time"""
    task = task_entry.get().strip()
    if not task:
        messagebox.showwarning("⚠️ Warning", "Please enter a task.")
        return
    time_added = datetime.now().strftime("%d %b %Y • %I:%M %p")
    add_task_ui(task, time_added)
    task_entry.delete(0, tk.END)
    save_tasks()

def add_task_ui(task, time_added, done=False):
    """Display task row with mark/done/delete"""
    container = tk.Frame(tasks_frame, bg="#ffffff", pady=6, highlightthickness=1, highlightbackground="#e1e1e1")
    container.pack(fill=tk.X, padx=10, pady=5)

    # Mark done toggle button
    mark_btn = tk.Button(
        container, text="✅" if done else "⬜",
        font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1abc9c",
        relief="flat", command=lambda c=container: toggle_done(c)
    )
    mark_btn.grid(row=0, column=0, rowspan=2, padx=(10, 5))

    # Task text
    task_label = tk.Label(
        container,
        text=("✅ " + task) if done else task,
        font=("Segoe UI Semibold", 13, "overstrike" if done else "normal"),
        bg="#ffffff", fg="#2c3e50" if not done else "#7f8c8d", anchor="w"
    )
    task_label.grid(row=0, column=1, sticky="w", padx=(5, 5))

    # Date & Time
    time_label = tk.Label(container, text=time_added, font=("Segoe UI", 9), bg="#ffffff", fg="#7f8c8d")
    time_label.grid(row=1, column=1, sticky="w", padx=(5, 5))

    # Delete button
    del_btn = tk.Button(
        container, text="🗑", font=("Segoe UI", 12, "bold"),
        bg="#ff4757", fg="white", activebackground="#e84118",
        relief="flat", width=3,
        command=lambda c=container: delete_task(c)
    )
    del_btn.grid(row=0, column=2, rowspan=2, padx=10)

    # store references
    container.mark_btn = mark_btn
    container.task_label = task_label
    container.time_label = time_label
    container.done = done

def toggle_done(container):
    """Toggle task between done / undone"""
    container.done = not container.done
    label = container.task_label
    btn = container.mark_btn
    if container.done:
        label.config(font=("Segoe UI Semibold", 13, "overstrike"), fg="#7f8c8d", text="✅ " + label.cget("text").replace("✅ ", ""))
        btn.config(text="✅")
    else:
        label.config(font=("Segoe UI Semibold", 13, "normal"), fg="#2c3e50", text=label.cget("text").replace("✅ ", ""))
        btn.config(text="⬜")
    save_tasks()

def delete_task(container):
    """Delete specific task"""
    container.destroy()
    save_tasks()

def clear_all():
    """Clear all tasks"""
    confirm = messagebox.askyesno("Confirm", "Delete all tasks?")
    if confirm:
        for widget in tasks_frame.winfo_children():
            widget.destroy()
        save_tasks()

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("🌈 Vibrant To-Do List")
root.geometry("520x620")
root.config(bg="#f0f3f5")
root.resizable(False, False)

# ---------- HEADER ----------
header = tk.Label(
    root, text="✨ My To-Do List",
    font=("Poppins SemiBold", 22, "bold"),
    bg="#f0f3f5", fg="#34495e"
)
header.pack(pady=20)

# ---------- ENTRY SECTION ----------
entry_frame = tk.Frame(root, bg="#f0f3f5")
entry_frame.pack(pady=10)

task_entry = tk.Entry(
    entry_frame, width=28, font=("Segoe UI", 14),
    bg="#ffffff", bd=2, relief="flat",
    highlightthickness=2, highlightbackground="#bdc3c7", highlightcolor="#1abc9c"
)
task_entry.grid(row=0, column=0, padx=10, ipady=8)

add_btn = tk.Button(
    entry_frame, text="➕ Add Task",
    font=("Segoe UI Semibold", 12),
    bg="#1abc9c", fg="white", activebackground="#16a085",
    relief="flat", padx=10, pady=8,
    command=add_task
)
add_btn.grid(row=0, column=1, padx=5)

# ---------- TASK LIST AREA ----------
list_frame = tk.Frame(root, bg="#f0f3f5")
list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tasks_canvas = tk.Canvas(list_frame, bg="#f0f3f5", highlightthickness=0)
tasks_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=tasks_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tasks_canvas.configure(yscrollcommand=scrollbar.set)

tasks_frame = tk.Frame(tasks_canvas, bg="#f0f3f5")
tasks_canvas.create_window((0, 0), window=tasks_frame, anchor="nw")

def on_configure(event):
    tasks_canvas.configure(scrollregion=tasks_canvas.bbox("all"))
tasks_frame.bind("<Configure>", on_configure)

# ---------- CLEAR ALL BUTTON ----------
clear_btn = tk.Button(
    root, text="🧹 Clear All", font=("Segoe UI Semibold", 12),
    bg="#f39c12", fg="white", relief="flat",
    padx=12, pady=8, activebackground="#e67e22",
    command=clear_all
)
clear_btn.pack(pady=10)

# ---------- FOOTER ----------
footer = tk.Label(
    root, text="💾 Auto-saved • ✅ Mark done • Vibrant Tkinter UI",
    font=("Segoe UI", 9),
    bg="#f0f3f5", fg="#7f8c8d"
)
footer.pack(side=tk.BOTTOM, pady=10)

# ---------- LOAD DATA ----------
load_tasks()

# ---------- RUN ----------
root.mainloop()
