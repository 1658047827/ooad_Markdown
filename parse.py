import re
from command import *


class Parse:
    def __init__(self, editor):
        self.editor = editor
        self.dispatcher = {
            "load": self.load,
            "save": self.save,
            "ws": self.ws,
            "switch": self.switch,
            "close": self.close,
            "insert": self.insert,
            "append-head": self.append_head,
            "append-tail": self.append_tail,
            "delete": self.delete,
            "undo": self.undo,
            "redo": self.redo,
            "list": self.list,
            "list-tree": self.list_tree,
            "dir-tree": self.dir_tree
        }

    def parse_input(self, input: str):
        command = None
        parts = input.split()
        handler = self.dispatcher.get(parts[0], None)
        if handler:
            command = handler(input)
        else:
            raise RuntimeError("Unknown command!")
        return command

    def load(self, input: str):
        pattern = re.compile(r"^load\s+(?P<file_path>.+)$")
        match = pattern.match(input)
        if match:
            file_path = match.group("file_path")
            return LoadCommand(self.editor, file_path)
        else:
            raise RuntimeError("Invalid command format!")

    def save(self, input: str):
        pattern = re.compile(r"^save$")
        match = pattern.match(input)
        if match:
            return SaveCommand(self.editor)
        else:
            raise RuntimeError("Invalid command format!")

    def ws(self, input: str):
        pattern = re.compile(r"^ws$")
        match = pattern.match(input)
        if match:
            return WsCommand(self.editor)
        else:
            raise RuntimeError("Invalid command format!")

    def switch(self, input: str):
        pattern = re.compile(r"^switch\s+(?P<file_num>\d+)$")
        match = pattern.match(input)
        if match:
            file_num = int(match.group("file_num"))
            return SwitchCommand(self.editor, file_num)
        else:
            raise RuntimeError("Invalid command format!")

    def close(self, input: str):
        pattern = re.compile(r"^close\s+(?P<file_num>\d+)$")
        match = pattern.match(input)
        if match:
            file_num = int(match.group("file_num"))
            return CloseCommand(self.editor, file_num)
        else:
            raise RuntimeError("Invalid command format!")

    def insert(self, input: str):
        pattern = re.compile(r"^insert\s+((?P<line_num>\d+)\s+)?(?P<content>.+)$")
        match = pattern.match(input)
        if match:
            content = match.group("content")
            line_num = match.group("line_num")
            line_num = int(line_num) if line_num else -1
            return InsertCommand(self.editor, line_num, content)
        else:
            raise RuntimeError("Invalid command format!")

    def append_head(self, input: str):
        pattern = re.compile(r"^append-head\s+(?P<content>.+)$")
        match = pattern.match(input)
        if match:
            content = match.group("content")
            return InsertCommand(self.editor, 1, content)
        else:
            raise RuntimeError("Invalid command format!")

    def append_tail(self, input: str):
        pattern = re.compile(r"^append-tail\s+(?P<content>.+)$")
        match = pattern.match(input)
        if match:
            content = match.group("content")
            return InsertCommand(self.editor, -1, content)
        else:
            raise RuntimeError("Invalid command format!")

    def delete(self, input: str):
        pattern = re.compile(r"^delete\s+((?P<line_num>\d+)|(?P<content>.+))$")
        match = pattern.match(input)
        if match:
            content = match.group("content")
            line_num = match.group("line_num")
            if line_num:
                line_num = int(line_num)
            return DeleteCommand(self.editor, line_num, content)
        else:
            raise RuntimeError("Invalid command format!")

    def undo(self, input: str):
        pattern = re.compile(r"^undo$")
        match = pattern.match(input)
        if match:
            pass
        else:
            raise RuntimeError("Invalid command format!")

    def redo(self, input: str):
        pattern = re.compile(r"^redo$")
        match = pattern.match(input)
        if match:
            pass
        else:
            raise RuntimeError("Invalid command format!")

    def list(self, input: str):
        pattern = re.compile(r"^list$")
        match = pattern.match(input)
        if match:
            pass
        else:
            raise RuntimeError("Invalid command format!")

    def list_tree(self, input: str):
        pattern = re.compile(r"^list-tree$")
        match = pattern.match(input)
        if match:
            pass
        else:
            raise RuntimeError("Invalid command format!")
        
    def dir_tree(self, input:str):
        pattern = re.compile(r"^dir-tree(\s+(?P<dir>.+))?$")
        match = pattern.match(input)
        if match:
            pass
        else:
            raise RuntimeError("Invalid command format!")
