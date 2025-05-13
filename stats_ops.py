# stats_ops.py (Fixed Count Visits)

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import simpledialog, messagebox, Tk
from utils import is_valid_date
import os

class StatsManager:
    def __init__(self, patient_file):
        self.patient_file = patient_file
        self.df = pd.DataFrame()
        self.load_data()

    def load_data(self):
        try:
            self.df = pd.read_csv(self.patient_file, dtype=str)
            self.df['Visit_time'] = pd.to_datetime(self.df['Visit_time'], errors='coerce')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load patient data: {e}")
            self.df = pd.DataFrame()

    def count_visits(self):
        root = Tk(); root.withdraw()
        self.load_data()

        date = simpledialog.askstring("Visit Date", "Enter date (YYYY-MM-DD):")
        if not is_valid_date(date):
            messagebox.showerror("Invalid Input", "Invalid date format.")
            return

        matches = self.df[self.df['Visit_time'].dt.strftime('%Y-%m-%d') == date.strip()]
        total = len(matches)
        unique_patients = matches['Patient_ID'].nunique()

        messagebox.showinfo("Visit Count", f"Date: {date}\nTotal Visits: {total}\nUnique Patients: {unique_patients}")

    def generate_stats(self):
        self.load_data()
        if self.df.empty:
            messagebox.showerror("Error", "No data loaded.")
            return

        try:
            os.makedirs("output", exist_ok=True)

            # 1. Visits by department
            dept_counts = self.df['Visit_department'].value_counts()
            dept_counts.plot(kind='bar', title='Visits by Department')
            plt.ylabel('Count')
            plt.tight_layout()
            plt.savefig("output/visits_by_department.png")
            plt.close()

            # 2. Gender distribution
            self.df['Gender'].value_counts().plot.pie(autopct='%1.1f%%', title='Gender Distribution')
            plt.ylabel('')
            plt.tight_layout()
            plt.savefig("output/gender_distribution.png")
            plt.close()

            # 3. Age distribution
            self.df['Age'].dropna().astype(float).plot.hist(bins=10, title='Age Distribution')
            plt.xlabel('Age')
            plt.ylabel('Frequency')
            plt.tight_layout()
            plt.savefig("output/age_distribution.png")
            plt.close()

            messagebox.showinfo("Statistics Generated", "Plots saved to /output folder.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate plots: {e}")
