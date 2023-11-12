from file import FileManager


class Editor:
    def __init__(self):
        self.file_manager = FileManager()
        self.current_md: list[str] = None

    def load(self, file_path):
        self.current_md = self.file_manager.load_file(file_path)

    def save(self):
        if self.current_md is None:
            raise RuntimeError("No currently open file.")
        file_num = self.file_manager.cur_file_num
        self.file_manager.save_file(file_num)

    def ws(self):
        self.file_manager.show_open_files()

    def switch(self, file_num):
        self.current_md = self.file_manager.switch_file(file_num)

    def close(self, file_num):
        self.current_md = self.file_manager.close_file(file_num)

    def insert(self, line_num, content):
        pass

    def delete(self):
        pass

    def list(self):
        if self.current_md is None:
            raise RuntimeError("No currently open file.")
        for line in self.current_md:
            print(line.strip("\r\n"))

    def list_tree(self):
        pass

    def exit(self):
        self.current_md = self.file_manager.close_all_files()
