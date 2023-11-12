class Command:
    def execute(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

    def __str__(self) -> str:
        # for debugging
        return str(self.__dict__)


class LoadCommand(Command):
    def __init__(self, editor, file_path):
        self.editor = editor
        self.file_path = file_path

    def execute(self):
        self.editor.load(self.file_path)


class SaveCommand(Command):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.save()


class WsCommand(Command):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.ws()


class SwitchCommand(Command):
    def __init__(self, editor, file_num):
        self.editor = editor
        self.file_num = file_num

    def execute(self):
        self.editor.switch(self.file_num)


class CloseCommand(Command):
    def __init__(self, editor, file_num):
        self.editor = editor
        self.file_num = file_num

    def execute(self):
        self.editor.close(self.file_num)


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


class ListCommand(Command):
    def __init__(self, editor):
        self.editor = editor

    def execute(self):
        self.editor.list()


class HistoryCommand(Command):
    def __init__(self, logger, record_num):
        self.logger = logger
        self.record_num = record_num

    def execute(self):
        pass


class StatsCommand(Command):
    pass
