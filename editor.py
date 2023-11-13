import re
import json
from file import FileManager


class Node:
    def __init__(self, level, content=None):
        self.level = level
        self.content = content
        self.children = []

    def add_child(self, child):
        self.children.append(child)


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
        if line_num == -1:
            self.current_md.append(f"{content}\n")
        elif 1 <= line_num and line_num <= len(self.current_md):
            self.current_md.insert(line_num - 1, f"{content}\n")
        else:
            raise RuntimeError("Invalid line number when inserting.")
        file_num = self.file_manager.cur_file_num
        self.file_manager.mark_modified(file_num)

    def delete(self, line_num, content):
        if line_num is not None:
            if 1 <= line_num and line_num <= len(self.current_md):
                self.current_md.pop(line_num - 1)
            else:
                raise RuntimeError("Invalid line number when deleting.")
        elif content is not None:
            escaped_content = re.escape(content)
            pattern_str = r"^((#+)|\*|-|\+|(\d+\.))\s+" + escaped_content + r"\n$"
            pattern = re.compile(pattern_str)

            for i in reversed(range(len(self.current_md))):
                if pattern.match(self.current_md[i]):
                    self.current_md.pop(i)

        file_num = self.file_manager.cur_file_num
        self.file_manager.mark_modified(file_num)

    def list(self):
        if self.current_md is None:
            raise RuntimeError("No currently open file.")
        for line in self.current_md:
            print(line.strip("\r\n"))

    def build_tree(self):
        root = Node(0, "root")
        node_list = [root]

        for line in self.current_md:
            header_pattern = re.compile(r"^(?P<header>#+)\s+(?P<content>.+)\n$")
            match = header_pattern.match(line)
            if match:
                header = match.group("header")
                content = match.group("content")
                level = len(header)
                node = Node(level, content)
            else:
                node = Node(8, line.strip("\r\n"))

            for n in reversed(node_list):
                if n.level < node.level:
                    n.add_child(node)
                    break
            node_list.append(node)

        return root

    def print_tree(self, node: Node, prefix):
        for i in range(len(node.children)):
            child = node.children[i]
            if i == len(node.children) - 1:
                print(f"{prefix}└── {child.content}")
                self.print_tree(child, prefix + "    ")
            else:
                print(f"{prefix}├── {child.content}")
                self.print_tree(child, prefix + "|   ")

    def list_tree(self):
        root = self.build_tree()
        self.print_tree(root, prefix="")

    def exit(self):
        self.current_md = self.file_manager.close_all_files()
