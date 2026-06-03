import re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

# --- تنظیمات ---
MASTER_FILE = "master.txt"
LINE_TO_UPDATE = 43 # ایندکس خط 44
TARGET_FILES = ["file1.txt", "file2.txt"] # فایل های مقصد برای sync
# --- پایان تنظیمات ---

def update_master_time(master_lines, line_index):
    if len(master_lines) <= line_index:
        print(f"Warning: master.txt has less than {line_index + 1} lines. Cannot update time.")
        return master_lines # یا می توانید خطا raise کنید

    current_line = master_lines[line_index]
    # استفاده از Regex برای پیدا کردن الگوی ساعت (XX:XX) و جایگزینی آن
    now = datetime.now(ZoneInfo("Asia/Tehran")).strftime("%H:%M")
    updated_line = re.sub(r'\d{2}:\d{2}', now, current_line)
    master_lines[line_index] = updated_line
    print(f"Updated line {line_index + 1} in master.txt with time: {now}")
    return master_lines

def sync_files(master_lines_content, target_files, line_index):
    if len(master_lines_content) <= line_index:
        print(f"Warning: master.txt content too short for sync. Skipping sync.")
        return

    # خطی که باید در فایل های مقصد کپی شود
    source_line_content = master_lines_content[line_index]
    
    for target_file_name in target_files:
        target_path = Path(target_file_name)
        if not target_path.exists():
            print(f"Warning: Target file {target_file_name} not found. Skipping.")
            continue
        
        target_lines = target_path.read_text(encoding="utf-8").splitlines()
        
        if len(target_lines) <= line_index:
            print(f"Warning: {target_file_name} has less than {line_index + 1} lines. Cannot sync line {line_index + 1}.")
            continue
        
        # جایگزینی خط در فایل مقصد
        target_lines[line_index] = source_line_content
        target_path.write_text("\n".join(target_lines) + "\n", encoding="utf-8")
        print(f"Synced line {line_index + 1} from master.txt to {target_file_name}")

# --- اجرای اصلی ---
master_file_path = Path(MASTER_FILE)
if not master_file_path.exists():
    print(f"Error: Master file '{MASTER_FILE}' not found!")
    exit(1)

# خواندن کل خطوط master.txt
master_lines = master_file_path.read_text(encoding="utf-8").splitlines()

# 1. آپدیت زمان در master.txt
updated_master_lines = update_master_time(master_lines, LINE_TO_UPDATE)

# نوشتن تغییرات master.txt
master_file_path.write_text("\n".join(updated_master_lines) + "\n", encoding="utf-8")

# 2. sync کردن تغییرات master.txt به فایل های دیگر
sync_files(updated_master_lines, TARGET_FILES, LINE_TO_UPDATE)

print("Process completed successfully.")

