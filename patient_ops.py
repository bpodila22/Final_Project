# patient_ops.py (Verified Working Logic)

import tkinter as tk
from tkinter import simpledialog, messagebox
import pandas as pd
import os
from utils import generate_visit_id, is_valid_date

class PatientManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_patient_data()

    def load_patient_data(self):
        if os.path.exists(self.file_path):
            self.df = pd.read_csv(self.file_path)
        else:
            self.df = pd.DataFrame(columns=[
                'Patient_ID', 'Visit_ID', 'Visit_time', 'Visit_department',
                'Race', 'Gender', 'Ethnicity', 'Age', 'Zip_code',
                'Insurance', 'Chief_complaint', 'Note_ID', 'Note_type'
            ])

    def save_data(self):
        self.df.to_csv(self.file_path, index=False)

    def add_patient(self):
        root = tk.Tk()
        root.withdraw()

        self.load_patient_data()
        pid = simpledialog.askstring("Patient ID", "Enter Patient ID:")
        if not pid:
            return

        pid = str(pid).strip()
        self.df['Patient_ID'] = self.df['Patient_ID'].astype(str).str.strip()
        existing = pid in self.df['Patient_ID'].values

        visit_time = simpledialog.askstring("Visit Date", "Enter Visit Date (YYYY-MM-DD):")
        if not is_valid_date(visit_time):
            messagebox.showerror("Error", "Invalid date format.")
            return

        visit_id = generate_visit_id(self.df['Visit_ID'].tolist())
        visit_dept = simpledialog.askstring("Visit Department", "Enter Department:")
        race = simpledialog.askstring("Race", "Enter Race:")
        gender = simpledialog.askstring("Gender", "Enter Gender:")
        ethnicity = simpledialog.askstring("Ethnicity", "Enter Ethnicity:")
        age = simpledialog.askinteger("Age", "Enter Age:")
        zip_code = simpledialog.askstring("Zip Code", "Enter Zip Code:")
        insurance = simpledialog.askstring("Insurance", "Enter Insurance Provider:")
        complaint = simpledialog.askstring("Chief Complaint", "Enter Chief Complaint:")
        note_id = simpledialog.askstring("Note ID", "Enter Note ID:")
        note_type = simpledialog.askstring("Note Type", "Enter Note Type:")

        record = {
            'Patient_ID': pid,
            'Visit_ID': visit_id,
            'Visit_time': visit_time,
            'Visit_department': visit_dept,
            'Race': race,
            'Gender': gender,
            'Ethnicity': ethnicity,
            'Age': age,
            'Zip_code': zip_code,
            'Insurance': insurance,
            'Chief_complaint': complaint,
            'Note_ID': note_id,
            'Note_type': note_type
        }

        self.df = pd.concat([self.df, pd.DataFrame([record])], ignore_index=True)
        self.save_data()
        messagebox.showinfo("Success", f"{'New patient added.' if not existing else 'Visit added to existing patient.'}")

    def remove_patient(self):
        self.load_patient_data()
        root = tk.Tk()
        root.withdraw()
        pid = simpledialog.askstring("Remove Patient", "Enter Patient ID to remove:")
        if not pid:
            return

        pid = str(pid).strip()
        self.df['Patient_ID'] = self.df['Patient_ID'].astype(str).str.strip()
        if pid not in self.df['Patient_ID'].values:
            messagebox.showwarning("Not Found", f"Patient ID {pid} not found.")
            return

        self.df = self.df[self.df['Patient_ID'] != pid]
        self.save_data()
        messagebox.showinfo("Removed", f"All records for Patient ID {pid} removed.")

    def retrieve_patient(self):
        self.load_patient_data()
        root = tk.Tk()
        root.withdraw()
        pid = simpledialog.askstring("Retrieve Patient", "Enter Patient ID:")
        if not pid:
            return

        pid = str(pid).strip()
        self.df['Patient_ID'] = self.df['Patient_ID'].astype(str).str.strip()
        matches = self.df[self.df['Patient_ID'] == pid]

        if matches.empty:
            messagebox.showinfo("Not Found", f"No data for Patient ID {pid}.")
            return

        try:
            matches['Visit_time'] = pd.to_datetime(matches['Visit_time'], errors='coerce')
            latest = matches.sort_values(by='Visit_time').dropna().iloc[-1]
        except:
            latest = matches.iloc[-1]

        info = (
            f"Patient ID: {latest['Patient_ID']}\n"
            f"Gender: {latest['Gender']}\nRace: {latest['Race']}\n"
            f"Ethnicity: {latest['Ethnicity']}\nAge: {latest['Age']}\n"
            f"Zip: {latest['Zip_code']}\nInsurance: {latest['Insurance']}\n"
            f"Visit Date: {latest['Visit_time']}\nDepartment: {latest['Visit_department']}\n"
            f"Chief Complaint: {latest['Chief_complaint']}\nNote ID: {latest['Note_ID']}\nNote Type: {latest['Note_type']}"
        )
        messagebox.showinfo("Patient Info", info)
