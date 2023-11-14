class Command:
    def execute(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass


class LoadCommand(Command):
    def __init__(self, editor, file_path):
        self.editor = editor
        self.file_path = file_path

    def execute(self):
        self.editor.load(self.file_path)

    def __str__(self) -> str:
        return f"load {self.file_path}"


class SaveCommand(Command):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.save()

    def __str__(self) -> str:
        return "save"


class WsCommand(Command):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.ws()

    def __str__(self) -> str:
        return "ws"


class SwitchCommand(Command):
    def __init__(self, editor, file_num):
        self.editor = editor
        self.file_num = file_num

    def execute(self):
        self.editor.switch(self.file_num)

    def __str__(self) -> str:
        return f"switch {self.file_num}"


class CloseCommand(Command):
    def __init__(self, editor, file_num):
        self.editor = editor
        self.file_num = file_num

    def execute(self):
        self.editor.close(self.file_num)

    def __str__(self) -> str:
        return f"close {self.file_num}"


class InsertCommand(Command):
    def __init__(self, editor, line_num, content):
        self.editor = editor
        self.line_num = line_num
        self.content = content

    def execute(self):
        self.editor.insert(self.line_num, self.content)

    def __str__(self) -> str:
        if self.line_num == -1:
            return f"insert {self.content}"
        else:
            return f"insert {self.line_num} {self.content}"


class AppendHeadCommand(Command):
    def __init__(self, editor, content):
        self.editor = editor
        self.content = content

    def execute(self):
        self.editor.insert(1, self.content)

    def __str__(self) -> str:
        return f"append-head {self.content}"


class AppendTailCommand(Command):
    def __init__(self, editor, content):
        self.editor = editor
        self.content = content

    def execute(self):
        self.editor.insert(-1, self.content)

    def __str__(self) -> str:
        return f"append-tail {self.content}"


class DeleteCommand(Command):
    def __init__(self, editor, line_num, content):
        self.editor = editor
        self.line_num = line_num
        self.content = content

    def execute(self):
        self.editor.delete(self.line_num, self.content)

    def __str__(self) -> str:
        if self.line_num is not None:
            return f"delete {self.line_num}"
        else:
            return f"delete {self.content}"


class ListCommand(Command):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.list()

    def __str__(self) -> str:
        return "list"


class ListTreeCommand(Command):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.list_tree()

    def __str__(self) -> str:
        return "list-tree"


class DirTreeCommand(Command):
    def __init__(self, editor, dir):
        self.editor = editor
        self.dir = dir

    def execute(self):
        if self.dir is None:
            self.editor.list_tree()
        else:
            self.editor.dir_tree(self.dir)

    def __str__(self) -> str:
        if self.dir is None:
            return "dir-tree"
        else:
            return f"dir-tree {self.dir}"


class HistoryCommand(Command):
    def __init__(self, logger, record_num):
        self.logger = logger
        self.record_num = record_num

    def execute(self):
        self.logger.history(self.record_num)

    def __str__(self) -> str:
        if self.record_num is None:
            return "history"
        else:
            return f"history {self.record_num}"


class StatsCommand(Command):
    def __init__(self, option):
        self.option = option

    def execute(self):
        pass

    def __str__(self) -> str:
        if self.option is None:
            return "stats"
        else:
            return f"stats {self.option}"
