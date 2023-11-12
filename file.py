import os


class FileManager:
    def __init__(self):
        self.cur_file_num = 0
        self.files = []

    def load_file(self, file_path):
        file_name = os.path.basename(file_path)
        for file in self.files:
            if file["name"] == file_name and os.path.samefile(file["path"], file_path):
                raise RuntimeError("The target file is already open.")

        if os.path.isfile(file_path):
            f = open(file_path, "r+", encoding="utf-8")
        else:
            f = open(file_path, "a+", encoding="utf-8")

        self.files.append(
            {
                "name": file_name,
                "path": file_path,
                "wrapper": f,
                "buffer": f.readlines(),
                "modified": False,
            }
        )
        self.cur_file_num = len(self.files)
        return self.files[-1]["buffer"]

    def save_file(self, file_num):
        self.check_file_num(file_num)
        file = self.files[file_num]

        # TODO

        file["modified"] = False

    def show_open_files(self):
        for i in range(len(self.files)):
            file = self.files[i]
            if i == (self.cur_file_num - 1):
                print(f"{i+1} {file['name']}{'*' if file['modified'] else ''}<")
            else:
                print(f"{i+1} {file['name']}{'*' if file['modified'] else ''}")

    def switch_file(self, file_num):
        self.check_file_num(file_num)
        self.cur_file_num = file_num
        return self.files[file_num - 1]["buffer"]

    def close_file(self, file_num):
        self.check_file_num(file_num)
        file = self.files[file_num - 1]
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
        file["wrapper"].close()
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

        if self.cur_file_num >= 1:
            return self.files[self.cur_file_num - 1]["buffer"]
        else:
            return None

    def close_all_files(self):
        for file_numn in range(len(self.files), 0, -1):
            self.close_file(file_numn)
        return None

    def check_file_num(self, file_num):
        if 1 > file_num or file_num > len(self.files):
            raise IndexError("File number does not exist.")
