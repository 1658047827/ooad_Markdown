class Invoker:
    def __init__(self, logger) -> None:
        self.logger = logger

    def execute_command(self, command):
        command.execute()
        self.logger.record_command(command)