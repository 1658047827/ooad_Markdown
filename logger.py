import logging
import datetime


class Logger:
    def __init__(self) -> None:
        self.logger = None

    def setup_logger(self):
        logger = logging.getLogger("history")
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler("history.log", encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        self.logger = logger

    def start_session(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
        log_entry = f"session start at {timestamp}"
        self.logger.info(log_entry)

    def record_command(self, command):
        timestamp = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
        log_entry = f"{timestamp} {command}"
        self.logger.info(log_entry)

    def history(self, record_num):
        with open("history.log", "r", encoding="utf-8") as file:
            lines = file.readlines()
        count = 0
        for i in reversed(range(len(lines))):
            line = lines[i]
            if line.startswith("session start at"):
                continue
            print(line.rstrip("\r\n"))
            count += 1
            if count == record_num:
                break

    def clean(self):
        for handler in self.logger.handlers[:]:
            handler.flush()
            handler.close()
            self.logger.removeHandler(handler)


logger_instance = Logger()
