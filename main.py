from parse import Parse


def client():
    # editor = Editor()
    editor = None
    parse = Parse(editor)

    print("Command Line Markdown Editing Tool")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        try:
            command = parse.parse_input(user_input)
        except RuntimeError as e:
            print(e)
            continue
        # command.execute()
        print(command)


if __name__ == "__main__":
    client()
