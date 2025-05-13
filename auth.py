# auth.py

import csv
import os

def verify_user(username, password, credentials_path):
    if not os.path.exists(credentials_path):
        print("Credentials file not found.")
        return None

    try:
        with open(credentials_path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'].strip() == username and row['password'].strip() == password:
                    return {
                        'username': username,
                        'role': row['role'].strip().lower()
                    }
    except Exception as e:
        print(f"Error reading credentials file: {e}")
        return None

    return None
