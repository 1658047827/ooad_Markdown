from parse import Parse
from editor import Editor
from logger import Logger
from invoker import Invoker


def client():
    editor = Editor()
    logger = Logger()
    invoker = Invoker(logger)
    parse = Parse(editor, logger, invoker)
    logger.start_session()

    print("Command Line Markdown Editing Tool")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            editor.exit()
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


if __name__ == "__main__":
    client()
