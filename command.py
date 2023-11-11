class Command:
    def execute(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass


class LoadCommand(Command):
    def __init__(self, editor, file_path):
        pass


class SaveCommand(Command):
    def __init__(self):
        pass