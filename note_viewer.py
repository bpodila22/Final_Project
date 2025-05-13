# note_viewer.py (Final Fix)

import pandas as pd
from tkinter import simpledialog, messagebox, Tk
from utils import is_valid_date

class NoteViewer:
    def __init__(self, patient_file, notes_file):
        self.patient_file = patient_file
        self.notes_file = notes_file

    def load_data(self):
        try:
            self.patients = pd.read_csv(self.patient_file, parse_dates=['Visit_time'])
            self.notes = pd.read_csv(self.notes_file)
        except Exception as e:
            messagebox.showerror("Load Error", f"Error loading files: {e}")
            self.patients = pd.DataFrame()
            self.notes = pd.DataFrame()

    def display_note(self):
        root = Tk(); root.withdraw()
        self.load_data()

        pid = simpledialog.askstring("View Note", "Enter Patient ID:")
        date = simpledialog.askstring("View Note", "Enter Visit Date (YYYY-MM-DD):")

        if not pid or not date:
            messagebox.showwarning("Missing Input", "Please enter both Patient ID and Date.")
            return

        if not is_valid_date(date):
            messagebox.showerror("Date Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        self.patients['Patient_ID'] = self.patients['Patient_ID'].astype(str).str.strip()
        self.patients['Visit_time'] = pd.to_datetime(self.patients['Visit_time'], errors='coerce')

        matches = self.patients[
            (self.patients['Patient_ID'] == pid.strip()) &
            (self.patients['Visit_time'].dt.strftime('%Y-%m-%d') == date.strip())
        ]

        if matches.empty:
            messagebox.showinfo("No Visit Found", "No patient visit found for given ID and date.")
            return

        found = False
        display = ""
        for _, row in matches.iterrows():
            note_id = str(row.get("Note_ID", "")).strip()
            note_type = row.get("Note_type", "N/A")

            match = self.notes[self.notes['Note_ID'].astype(str).str.strip() == note_id]
            if not match.empty:
                note_text = match.iloc[0].get("Note_text", "No text available.")
                display += f"Note ID: {note_id}\nNote Type: {note_type}\nNote Text:\n{note_text}\n{'-'*40}\n"
                found = True

        if found:
            messagebox.showinfo("Note Found", display)
        else:
            messagebox.showwarning("Note Missing", "No matching note text found in Notes.csv.")