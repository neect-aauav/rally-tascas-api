from datetime import datetime

class Logger:

    def __init__(self, path):
        self.path = path

    def __write(self, file, prefix, message):
        with open(file, 'a') as f:
            f.write(f"[{prefix}]: {message}\n")

    def __build(self, token, prefix, msg):
        file = self.path + token + ".log"
        prefix = f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - {prefix}"
        self.__write(file, prefix, msg)

    def info(self, token, msg):
        self.__build(token, "INFO", msg)

    def warning(self, token, msg):
        self.__build(token, "WARNING", msg)

    def error(self, token, msg):
        self.__build(token, "ERROR", msg)

    def critical(self, token, msg):
        self.__build(token, "CRITICAL", msg)