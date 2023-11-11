from frontend import Frontend


def main():
    editor = Editor()
    frontend = Frontend(editor)

    while True:
        user_input = input("Enter a command (type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break
        args = frontend.parse_input(user_input.split())
        frontend.execute_command(args)


if __name__ == "__main__":
    main()
