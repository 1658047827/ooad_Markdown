class Command:
    def execute(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

    def __str__(self) -> str:
        return str(self.__dict__)


class LoadCommand(Command):
    def __init__(self, editor, file_path):
        self.editor = editor
        self.file_path = file_path

    def execute(self):
        pass


class SaveCommand(Command):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        pass


class WsCommand(Command):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        pass


class SwitchCommand(Command):
    def __init__(self, editor, file_num):
        self.editor = editor
        self.file_num = file_num

    def execute(self):
        pass


class CloseCommand(Command):
    def __init__(self, editor, file_num):
        self.editor = editor
        self.file_num = file_num

    def execute(self):
        pass


class InsertCommand(Command):
    def __init__(self, editor, line_num, content):
        self.editor = editor
        self.line_num = line_num
        self.content = content

    def execute(self):
        pass


class DeleteCommand(Command):
    def __init__(self, editor, line_num, content):
        self.editor = editor
        self.line_num = line_num
        self.content = content

    def execute(self):
        pass
