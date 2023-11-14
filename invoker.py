class Invoker:
    def __init__(self, logger) -> None:
        self.logger = logger
        self.undo_command = None
        self.redo_command = None

    def execute_command(self, command):
        command.execute()
        self.logger.record_command(command)
        if command.undoable():
            self.undo_command = command

    def undo(self):
        if self.undo_command is None:
            raise RuntimeError("No command to undo.")
        command = self.undo_command
        command.undo()
        self.undo_command = None
        self.redo_command = command

    def redo(self):
        if self.redo_command is None:
            raise RuntimeError("No command to redo.")
        command = self.redo_command
        command.execute()
        self.redo_command = None
        self.undo_command = command