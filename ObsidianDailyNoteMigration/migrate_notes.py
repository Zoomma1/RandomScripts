import os
import shutil
from datetime import datetime

def create_folder_structure(base_path, date):
    year = date.strftime("%Y")
    month = date.strftime("%B")
    week = date.strftime("Week %U")

    year_folder = os.path.join(base_path, year)
    month_folder = os.path.join(year_folder, month)
    week_folder = os.path.join(month_folder, week)

    if not os.path.exists(year_folder):
        os.makedirs(year_folder)
    if not os.path.exists(month_folder):
        os.makedirs(month_folder)
    if not os.path.exists(week_folder):
        os.makedirs(week_folder)

    return week_folder

def migrate_notes(base_path):
    for filename in os.listdir(base_path):
        if filename.endswith(".md"):
            try:
                date_str = filename.split(".")[0]
                date = datetime.strptime(date_str, "%Y-%m-%d")

                week_folder = create_folder_structure(base_path, date)
                src_file = os.path.join(base_path, filename)
                dest_file = os.path.join(week_folder, filename)

                shutil.move(src_file, dest_file)
                print(f"Moved {filename} to {week_folder}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    base_path = "C:/Users/victo/OneDrive/Bureau/Tha vault/00 - Daily notes"
    migrate_notes(base_path)
