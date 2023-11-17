import logging
from parse import Parse
from editor import editor_instance
from logger import logger_instance
from invoker import invoker_instance
from stats import stats_instance
from file import file_manager_instance


def client():
    stats_instance.setup_logger()
    logger_instance.setup_logger()
    file_manager_instance.attach(stats_instance)
    editor_instance.set_file_manager(file_manager_instance)
    invoker_instance.set_logger(logger_instance)
    parse = Parse(
        editor_instance,
        logger_instance,
        invoker_instance,
        stats_instance,
        file_manager_instance,
    )

    logger_instance.start_session()
    stats_instance.start_session()

    print("Command Line Markdown Editing Tool")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        try:
            command = None
            command = parse.parse_input(user_input)
            invoker_instance.execute_command(command)
        except Exception as e:
            print(e)
            if command is not None:
                logger_instance.record_command(command)
            continue

    editor_instance.exit()
    logger_instance.clean()
    stats_instance.clean()
    logging.shutdown()


if __name__ == "__main__":
    client()
