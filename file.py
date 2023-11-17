import os
from datetime import datetime, timedelta


class FileManager:
    def __init__(self):
        self.cur_file_num = 0
        self.last_timestamp = None
        self.files = []
        self.stats = None

    def attach(self, stats):
        self.stats = stats

    def notify(self):
        if self.cur_file_num <= 0:
            raise RuntimeError("No currently open file.")
        file_path = self.files[self.cur_file_num - 1]["path"]
        self.stats.update(file_path, datetime.now() - self.last_timestamp)
        self.last_timestamp = datetime.now()

    def load_file(self, file_path):
        file_name = os.path.basename(file_path)
        for file in self.files:
            if file["name"] == file_name and os.path.samefile(file["path"], file_path):
                raise RuntimeError("The target file is already open.")

        isfile = os.path.isfile(file_path)
        if isfile:
            file = open(file_path, "r", encoding="utf-8")
        else:
            file = open(file_path, "a+", encoding="utf-8")
        self.files.append(
            {
                "name": file_name,
                "path": file_path,
                "buffer": file.readlines(),
                "modified": not isfile,
                "new": not isfile,
            }
        )
        file.close()

        if self.last_timestamp is not None:
            self.notify()
        else:
            self.last_timestamp = datetime.now()
        self.cur_file_num = len(self.files)
        return self.files[-1]["buffer"]

    def save_file(self, file_num):
        self.check_file_num(file_num)
        file = self.files[file_num - 1]
        with open(file["path"], "w", encoding="utf-8") as f:
            f.writelines(file["buffer"])
        file["modified"] = False
        file["new"] = False

    def show_open_files(self):
        for i in range(len(self.files)):
            file = self.files[i]
            if i == (self.cur_file_num - 1):
                print(f"{i+1} {file['name']}{'*' if file['modified'] else ''}<")
            else:
                print(f"{i+1} {file['name']}{'*' if file['modified'] else ''}")

    def switch_file(self, file_num):
        self.check_file_num(file_num)
        self.notify()
        self.cur_file_num = file_num
        return self.files[file_num - 1]["buffer"]

    def close_file(self, file_num):
        self.check_file_num(file_num)
        file = self.files[file_num - 1]

        if file_num == self.cur_file_num:
            self.notify()

        if file["modified"]:
            while True:
                choice = input(
                    f"Save changed file {file['name']} before closing? (y/n) "
                ).lower()
                if choice == "y" or choice == "n":
                    break
                else:
                    print("Please input a valid option, 'y' or 'n'.")
            if choice == "y":
                self.save_file(file_num)
            elif choice == "n" and file["new"]:
                os.remove(file["path"])
        self.stats.flush(file["path"])
        self.files.pop(file_num - 1)

        if file_num < self.cur_file_num:
            self.cur_file_num -= 1
        elif file_num == self.cur_file_num:
            if file_num > 1:
                self.cur_file_num -= 1
            elif file_num == 1 and len(self.files) >= 1:
                self.cur_file_num = 1
            else:
                self.cur_file_num = 0
                self.last_timestamp = None

        if self.cur_file_num >= 1:
            return self.files[self.cur_file_num - 1]["buffer"]
        else:
            return None

    def close_all_files(self):
        for file_num in range(len(self.files), 0, -1):
            self.close_file(file_num)
        return None

    def check_file_num(self, file_num):
        if 1 > file_num or file_num > len(self.files):
            raise IndexError("File number does not exist.")

    def mark_modified(self, file_num):
        self.check_file_num(file_num)
        self.files[file_num - 1]["modified"] = True

    def get_cur_file_path(self):
        if self.cur_file_num <= 0:
            raise RuntimeError("No currently open file.")
        return self.files[self.cur_file_num - 1]["path"]
