import os
import re
import argparse
from datetime import datetime

def clean_file_name(file_name, date_str):
    name, ext = os.path.splitext(file_name)
    clean_name = re.sub(r'[a-fA-F0-9]{32}$', '', name).strip()
    new_name = f"{clean_name} {date_str}".strip() + ext
    return new_name

def rename_files(directory, output_directory, use_date):
    os.makedirs(output_directory, exist_ok=True)

    for root, dirs, files in os.walk(directory):
        for file in files:
            original_path = os.path.join(root, file)
            try:
                if use_date:
                    date_str = extract_date_from_file(original_path)
                else:
                    date_str = ""
                cleaned_name = clean_file_name(file, date_str)
                cleaned_path = os.path.join(output_directory, cleaned_name)
                os.rename(original_path, cleaned_path)
            except KeyError:
                print(f"Skipping {file}: 'Date' not found in frontmatter.")
            except Exception as e:
                print(f"Error processing {file}: {e}")

    print("File renaming completed.")

def extract_date_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        date_match = re.search(r'Date:\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})', content)
        if not date_match:
            raise KeyError('Date not found in frontmatter')

        date_str = date_match.group(1)
        date_obj = datetime.strptime(date_str, '%B %d, %Y')
        formatted_date_str = date_obj.strftime('%Y-%m-%d')
        return formatted_date_str

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rename files in a directory by removing trailing random characters and adding a date.')
    parser.add_argument('directory', type=str, help='The directory containing the files to rename')
    parser.add_argument('output_directory', type=str, help='The directory to save the renamed files')
    parser.add_argument('--date', action='store_true', help='If enabled, the script will extract the date from the file content and use it to rename the file.')
    args = parser.parse_args()

    rename_files(args.directory, args.output_directory, args.date)
