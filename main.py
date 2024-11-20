# -*- coding: utf-8 -*-

import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
import time

# 存放已知病毒文件的MD5值
md5list = []
# 存放找到的病毒文件名称
fnameList = []
# 存放匹配的文件数量
md5num = 0
# 记录共扫描的文件数量
file_num = 0


# 读取配置文件内容
def read_md5_list():
    global md5list
    try:
        with open('md5v.ini') as file:
            content = file.readlines()
            for l in content:
                _l = l.strip()
                if len(_l) > 0:
                    md5list.append(l.rstrip())
    except FileNotFoundError:
        messagebox.showerror("Error", "MD5 configuration file not found")
        exit()


# 遍历文件目录及子目录中的文件
def scan_files(path):
    global md5num, fnameList, file_num
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_num += 1
            tmp_filename = os.path.join(dirpath, filename)
            try:
                with open(tmp_filename, 'rb') as fp:
                    data = fp.read()
                    file_md5 = hashlib.md5(data).hexdigest()
                    if file_md5 in md5list:
                        md5num += 1
                        fnameList.append(tmp_filename)
            except Exception as e:
                print(f"Error scanning file {tmp_filename}: {e}")


# 执行扫描
def perform_scan():
    path = app.path_entry.get()  # Use app to access path_entry
    if not path:
        messagebox.showerror("Error", "Please select a path")
        return
    global md5num, fnameList, file_num
    md5num = 0
    fnameList = []
    file_num = 0

    read_md5_list()  # Read MD5 list

    start_time = time.time()  # Record start time
    scan_files(path)  # Execute scan
    end_time = time.time()  # Record end time

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)

    results = f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}\n"
    results += f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}\n"
    results += f"Total Files Scanned: {file_num}\n"
    results += f"Matched Files: {md5num}\n"
    results += "Matched Files:\n"
    for fn in fnameList:
        results += f"{fn}\n"
    results += f"Elapsed Time: {elapsed_minutes} min {elapsed_seconds} sec"

    app.results_label.config(text=results)  # Access results_label through app


class VirusScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Virus Scanner")

        self.path_label = tk.Label(root, text="Scan Path:")
        self.path_label.pack()
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack()
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_folder)
        self.browse_button.pack()

        self.scan_button = tk.Button(root, text="Start Scan", command=perform_scan)
        self.scan_button.pack()

        self.results_label = tk.Label(root, text="", justify=tk.LEFT)
        self.results_label.pack()

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, folder_selected)


if __name__ == "__main__":
    root = tk.Tk()
    app = VirusScannerGUI(root)
    root.mainloop()