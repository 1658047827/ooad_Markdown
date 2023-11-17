import logging
from parse import Parse
from editor import Editor
from logger import Logger
from invoker import Invoker
from stats import Stats
from file import FileManager


def client():
    stats = Stats()
    logger = Logger()
    file_manager = FileManager()
    file_manager.attach(stats)
    editor = Editor(file_manager)
    invoker = Invoker(logger)
    parse = Parse(editor, logger, invoker, stats, file_manager)

    logger.start_session()
    stats.start_session()
    
    print("Command Line Markdown Editing Tool")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        try:
            command = None
            command = parse.parse_input(user_input)
            invoker.execute_command(command)
        except Exception as e:
            print(e)
            if command is not None:
                logger.record_command(command)
            continue
    
    editor.exit()
    logger.clean()
    stats.clean()
    logging.shutdown()


if __name__ == "__main__":
    client()
