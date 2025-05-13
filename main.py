# main.py

import tkinter as tk
from app_gui import ClinicalDataApp


def launch_app():
    window = tk.Tk()
    window.title("Clinical Data Warehouse")
    window.geometry("600x400")
    app = ClinicalDataApp(window)
    window.mainloop()


if __name__ == "__main__":
    launch_app()