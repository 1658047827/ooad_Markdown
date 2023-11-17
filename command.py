class Command:
    def execute(self):
        pass

    def can_undo(self):
        return False

    def can_ignore(self):
        return False


class CanIgnoreCommand(Command):
    def can_ignore(self):
        return True


class CanUndoCommand(Command):
    def can_undo(self):
        return True

    def undo(self):
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


class InsertCommand(CanUndoCommand):
    def __init__(self, editor, line_num, content):
        self.editor = editor
        self.line_num = line_num
        self.content = content
        self.inserted_line = -1

    def execute(self):
        self.inserted_line = self.editor.insert(self.line_num, self.content)

    def undo(self):
        self.editor.delete(self.inserted_line, None)

    def __str__(self) -> str:
        if self.line_num == -1:
            return f"insert {self.content}"
        else:
            return f"insert {self.line_num} {self.content}"


class AppendHeadCommand(CanUndoCommand):
    def __init__(self, editor, content):
        self.editor = editor
        self.content = content
        self.inserted_line = -1

    def execute(self):
        self.inserted_line = self.editor.insert(1, self.content)

    def undo(self):
        self.editor.delete(self.inserted_line, None)

    def __str__(self) -> str:
        return f"append-head {self.content}"


class AppendTailCommand(CanUndoCommand):
    def __init__(self, editor, content):
        self.editor = editor
        self.content = content
        self.inserted_line = -1

    def execute(self):
        self.inserted_line = self.editor.insert(-1, self.content)

    def undo(self):
        self.editor.delete(self.inserted_line, None)

    def __str__(self) -> str:
        return f"append-tail {self.content}"


class DeleteCommand(CanUndoCommand):
    def __init__(self, editor, line_num, content):
        self.editor = editor
        self.line_num = line_num
        self.content = content
        self.deleted_lines = None

    def execute(self):
        self.deleted_lines = self.editor.delete(self.line_num, self.content)

    def undo(self):
        for line_num, content in self.deleted_lines:
            self.editor.insert(line_num, content)

    def __str__(self) -> str:
        if self.line_num is not None:
            return f"delete {self.line_num}"
        else:
            return f"delete {self.content}"


class UndoCommand(CanIgnoreCommand):
    def __init__(self, invoker):
        self.invoker = invoker

    def execute(self):
        self.invoker.undo()

    def __str__(self) -> str:
        return "undo"


class RedoCommand(CanIgnoreCommand):
    def __init__(self, invoker):
        self.invoker = invoker

    def execute(self):
        self.invoker.redo()

    def __str__(self) -> str:
        return "redo"


class ListCommand(CanIgnoreCommand):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.list()

    def __str__(self) -> str:
        return "list"


class ListTreeCommand(CanIgnoreCommand):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.list_tree()

    def __str__(self) -> str:
        return "list-tree"


class DirTreeCommand(CanIgnoreCommand):
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


class HistoryCommand(CanIgnoreCommand):
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


class StatsCommand(CanIgnoreCommand):
    def __init__(self, file_manager, stats_module, option):
        self.file_manager = file_manager
        self.stats_module = stats_module
        self.option = option

    def execute(self):
        self.file_manager.notify()
        file_path = self.file_manager.get_cur_file_path()
        if self.option == "all":
            self.stats_module.display_stats("all", None)
        else:
            self.stats_module.display_stats("current", file_path)

    def __str__(self) -> str:
        if self.option is None:
            return "stats"
        else:
            return f"stats {self.option}"
