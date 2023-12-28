import re
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
        self.file_manager = None
        self.current_md: list[str] = None

    def set_file_manager(self, file_manager: FileManager):
        self.file_manager = file_manager

    def set_md(self, md):
        self.current_md = md

    def insert(self, line_num, content) -> int:
        if self.current_md is None:
            raise RuntimeError("No currently open file.")
        if line_num == -1:
            self.current_md.append(f"{content}\n")
        elif 1 <= line_num and line_num <= len(self.current_md) + 1:
            self.current_md.insert(line_num - 1, f"{content}\n")
        else:
            raise RuntimeError("Invalid line number when inserting.")
        file_num = self.file_manager.cur_file_num
        self.file_manager.mark_modified(file_num)

        if line_num == -1:
            return len(self.current_md)
        else:
            return line_num

    def delete(self, line_num, content):
        if self.current_md is None:
            raise RuntimeError("No currently open file.")
        if line_num is not None:
            if 1 <= line_num and line_num <= len(self.current_md):
                line = self.current_md.pop(line_num - 1)
            else:
                raise RuntimeError("Invalid line number when deleting.")
        elif content is not None:
            escaped_content = re.escape(content)
            pattern_str = r"^(((#+)|\*|-|\+|(\d+\.))\s+)?" + escaped_content + r"\n$"
            pattern = re.compile(pattern_str)
            deleted_lines = []

            for i in reversed(range(len(self.current_md))):
                if pattern.match(self.current_md[i]):
                    line = self.current_md.pop(i)
                    deleted_lines.append((i + 1, line))
            deleted_lines.reverse()

        file_num = self.file_manager.cur_file_num
        self.file_manager.mark_modified(file_num)

        if line_num is not None:
            return [(line_num, line)]
        else:
            return deleted_lines

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
                header, content = match.groups()
                level = len(header)
                node = Node(level, content)
            else:
                node = Node(8, line.strip("\r\n"))

            while len(node_list) > 0 and node_list[-1].level >= node.level:
                node_list.pop()
            if len(node_list) > 0:
                node_list[-1].add_child(node)

            node_list.append(node)

        return root

    def print_tree(self, node: Node, prefix):
        pattern_str = r"^(\*|-|\+) "
        pattern = re.compile(pattern_str)
        for i in range(len(node.children)):
            child = node.children[i]
            if pattern.match(child.content):
                child.content = "·" + child.content[1:]
            if i == len(node.children) - 1:
                print(f"{prefix}└── {child.content}")
                self.print_tree(child, prefix + "    ")
            else:
                print(f"{prefix}├── {child.content}")
                self.print_tree(child, prefix + "│   ")

    def find_dir(self, node: Node, dir):
        if node.level <= 8 and node.content == dir:
            return node
        for child in node.children:
            n = self.find_dir(child, dir)
            if n is not None:
                return n
        return None

    def list_tree(self):
        if self.current_md is None:
            raise RuntimeError("No currently open file.")
        root = self.build_tree()
        self.print_tree(root, prefix="")

    def dir_tree(self, dir):
        if self.current_md is None:
            raise RuntimeError("No currently open file.")
        root = self.build_tree()
        node = self.find_dir(root, dir)
        if node is None:
            raise RuntimeError("The specified dir is not found.")
        else:
            print(f"└── {node.content}")
            self.print_tree(node, prefix="    ")

    def exit(self):
        self.current_md = self.file_manager.close_all_files()


editor_instance = Editor()
