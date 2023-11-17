from command import *


class Invoker:
    def __init__(self) -> None:
        self.logger = None
        self.undo_command = None
        self.redo_command = None

    def set_logger(self, logger):
        self.logger = logger

    def execute_command(self, command):
        command.execute()
        self.logger.record_command(command)
        if command.can_undo():  # insert, delete
            self.undo_command = command
            self.redo_command = None
        elif command.can_ignore():  # list, list-tree
            return
        elif not command.can_ignore():  # save, load
            self.undo_command = None

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


invoker_instance = Invoker()
