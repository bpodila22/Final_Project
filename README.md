# Final_Project
# Clinical Data Warehouse Application

A Tkinter-based clinical record management system for managing patient visits, clinical notes, and analytics. This project was developed for the **HI 741 Spring 2025 Final Project**.

---

## 🛠 How to Run the Application

1. Make sure you have Python 3.11+ installed.
2. Open terminal and navigate to the project folder:
3. Run the application using:
   ```bash
   python main.py
   ```
4. Login with credentials from `data/Credentials.csv`

### ✅ Required Python Libraries:
```bash
pip install pandas matplotlib
```

---

## 🗂 Project Structure
```
clinical_data_warehouse_App/
├── main.py
├── app_gui.py
├── auth.py
├── patient_ops.py
├── stats_ops.py
├── note_viewer.py
├── utils.py
│
├── data/
│   ├── Credentials.csv
│   ├── Patient_data.csv
│   └── Notes.csv
│
├── output/
│   ├── usage_log.csv
│   ├── age_distribution.png
│   ├── gender_distribution.png
│   └── visits_by_department.png
│
├── 

```

---

## ✅ Functionalities (6 Actions)
| Function              | Who Can Access      |
|-----------------------|----------------------|
| Retrieve Patient       | Clinician, Nurse     |
| Add Patient            | Clinician, Nurse     |
| Remove Patient         | Clinician, Nurse     |
| View Note              | Clinician, Nurse     |
| Count Visits           | Admin, Clinician, Nurse |
| Generate Statistics    | Management           |

---

## 📄 Output Files
- **Patient_data.csv**: Automatically updated after each add/remove
- **usage_log.csv**: Logs all login attempts and actions (including failed ones)

---

## 📊 Statistics (saved in output/)
- `visits_by_department.png`
- `gender_distribution.png`
- `age_distribution.png`

---

## 👥 Roles Supported
- Clinician
- Nurse
- Admin
- Management

