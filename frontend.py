import argparse


class Frontend:
    def __init__(self, editor):
        self.editor = editor
        self.parser = argparse.ArgumentParser(description="Command-line Markdown editor tool.")

        subparsers = self.parser.add_subparsers(dest="command", help="Available commands.")

        # "load" command
        load_parser = subparsers.add_parser("load", help="Load a file")
        load_parser.add_argument("file_path", help="Path to the file")

        # "list" command
        subparsers.add_parser("list", help="List the content")

        # "list-tree" command
        subparsers.add_parser("list-tree", help="List the content in tree format")

        # "undo" command
        subparsers.add_parser("undo", help="Undo the last command")

        # "redo" command
        subparsers.add_parser("redo", help="Redo the last undone command")

    def parse_input(self, args):
        return self.parser.parse_args(args)

    def execute_command(self, args):
        # 执行相应的操作
        if args.command == "load":
            load_command = LoadCommand(self.editor, args.file_path)
            self.editor.execute_command(load_command)
        elif args.command == "list":
            list_command = ListCommand(self.editor)
            list_command.execute()
        elif args.command == "list-tree":
            list_tree_command = ListTreeCommand(self.editor)
            list_tree_command.execute()
        elif args.command == "undo":
            self.editor.undo()
        elif args.command == "redo":
            self.editor.redo()
        else:
            print(f"Unknown command: {args.command}")
