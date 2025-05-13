# app_gui.py (Updated with Logging)

import tkinter as tk
from tkinter import messagebox
import datetime
import os
import csv

from auth import verify_user
from patient_ops import PatientManager
from stats_ops import StatsManager
from note_viewer import NoteViewer


class ClinicalDataApp:
    def __init__(self, master):
        self.master = master
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.user_info = None

        self.patient_manager = PatientManager("data/Patient_data.csv")
        self.stats_manager = StatsManager("data/Patient_data.csv")
        self.note_viewer = NoteViewer("data/Patient_data.csv", "data/Notes.csv")

        self.build_login_ui()

    def build_login_ui(self):
        self.clear_window()
        tk.Label(self.master, text="Username").pack(pady=5)
        tk.Entry(self.master, textvariable=self.username_var).pack(pady=5)

        tk.Label(self.master, text="Password").pack(pady=5)
        tk.Entry(self.master, textvariable=self.password_var, show="*").pack(pady=5)

        tk.Button(self.master, text="Login", command=self.login_user).pack(pady=15)

    def login_user(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        result = verify_user(username, password, "data/Credentials.csv")
        self.user_info = result

        if result:
            self.log_event(username, result['role'], "Login Success")
            self.display_main_menu()
        else:
            self.log_event(username, "unknown", "Login Failed")
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def display_main_menu(self):
        self.clear_window()
        tk.Label(self.master, text=f"Welcome {self.user_info['username']} ({self.user_info['role']})", font=("Arial", 14)).pack(pady=10)

        role = self.user_info['role']
        actions = {
            "Retrieve Patient": lambda: self.wrap_action("Retrieve Patient", self.patient_manager.retrieve_patient),
            "Add Patient": lambda: self.wrap_action("Add Patient", self.patient_manager.add_patient),
            "Remove Patient": lambda: self.wrap_action("Remove Patient", self.patient_manager.remove_patient),
            "Count Visits": lambda: self.wrap_action("Count Visits", self.stats_manager.count_visits),
            "View Note": lambda: self.wrap_action("View Note", self.note_viewer.display_note),
            "Generate Stats": lambda: self.wrap_action("Generate Stats", self.stats_manager.generate_stats),
            "Exit": self.master.quit
        }

        visible_buttons = {
            "clinician": ["Retrieve Patient", "Add Patient", "Remove Patient", "Count Visits", "View Note", "Exit"],
            "nurse":     ["Retrieve Patient", "Add Patient", "Remove Patient", "Count Visits", "View Note", "Exit"],
            "admin":     ["Count Visits", "Exit"],
            "management":["Generate Stats", "Exit"]
        }

        for label in visible_buttons.get(role, []):
            tk.Button(self.master, text=label, width=30, command=actions[label]).pack(pady=4)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def wrap_action(self, action_name, func):
        try:
            func()
            self.log_event(self.user_info['username'], self.user_info['role'], action_name)
        except Exception as e:
            messagebox.showerror("Action Error", f"Failed to perform {action_name}: {e}")

    def log_event(self, username, role, action):
        os.makedirs("output", exist_ok=True)
        log_file = os.path.join("output", "usage_log.csv")

        entry = {
            "username": username,
            "role": role,
            "action": action,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        file_exists = os.path.exists(log_file)
        with open(log_file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=entry.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(entry)