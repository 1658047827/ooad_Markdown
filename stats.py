import logging
from datetime import datetime, timedelta
from collections import defaultdict


class Observer:
    def update(self, file_path, duration: timedelta):
        pass


class Stats(Observer):
    def __init__(self):
        self.session_start_timestamp = None
        self.logger = self.setup_logger()
        self.stats_data = defaultdict(timedelta)

    def setup_logger(self):
        logger = logging.getLogger("stats")
        logger.setLevel(logging.INFO)

        log_file_name = "stats.log"
        file_handler = logging.FileHandler(log_file_name, encoding="utf-8")
        file_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)

        return logger

    def start_session(self):
        timestamp = datetime.now().strftime("%Y%m%d %H:%M:%S")
        log_entry = f"session start {timestamp}"
        self.session_start_timestamp = timestamp
        self.logger.info(log_entry)

    def flush(self, file_path):
        formated_delta = self.format_timedelta(self.stats_data[file_path])
        log_entry = f"{file_path} {formated_delta}"
        self.logger.info(log_entry)
        self.stats_data.pop(file_path)

    def update(self, file_path, duration: timedelta):
        self.stats_data[file_path] += duration

    def display_stats(self, option, file_path):
        print(f"session start {self.session_start_timestamp}")
        if option == "all":
            for path, delta in self.stats_data.items():
                print(f"{path} {self.format_timedelta(delta)}")
        else:
            delta = self.stats_data[file_path]
            print(f"{file_path} {self.format_timedelta(delta)}")

    def format_timedelta(self, delta):
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days} 天 {hours} 小时 {minutes} 分钟 {seconds} 秒"
        elif hours > 0:
            return f"{hours} 小时 {minutes} 分钟 {seconds} 秒"
        elif minutes > 0:
            return f"{minutes} 分钟 {seconds} 秒"
        else:
            return f"{seconds} 秒"

    def clean(self):
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
