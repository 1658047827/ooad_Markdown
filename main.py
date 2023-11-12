from parse import Parse
from editor import Editor
from logger import Logger


def client():
    editor = Editor()
    logger = Logger()
    parse = Parse(editor, logger)

    print("Command Line Markdown Editing Tool")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            editor.exit()
            break
        try:
            command = parse.parse_input(user_input)
            # print(command) # for debugging
            command.execute()
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    client()
