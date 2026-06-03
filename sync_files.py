import os

def sync():
    # خواندن محتوای مرجع
    with open('master.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # استخراج خط ۱۰ تا ۵۰ (ایندکس ۹ تا ۴۹)
        new_content = lines[9:50]

    # لیست فایل‌هایی که باید آپدیت شوند
    files = ['file1.txt', 'file2.txt'] 

    for file_name in files:
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.readlines()
            
            # بازسازی فایل: خطوط ۱ تا ۹ + محتوای جدید + خطوط ۵۱ به بعد
            updated = content[:9] + new_content + content[50:]
            
            with open(file_name, 'w', encoding='utf-8') as f:
                f.writelines(updated)

if __name__ == "__main__":
    sync()
