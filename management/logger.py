from datetime import datetime


class Logger:

    def __init__(self, path):
        self.path = path

    def __write(self, token, prefix, message):
        time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        splitted = message.split("]@")
        status = message.split("]@")[0][1:]

        # dump log to database model
        from management.models import DBLogger
        log = DBLogger(user=token, type=prefix, time=time, status=status, message=splitted[1])
        log.save()

        file = self.path + token + ".log"
        with open(file, 'a') as f:
            f.write(f"[{time} - {prefix}]: {message}\n")

    def __build(self, token, prefix, msg):
        token = token
        self.__write(token, prefix, msg)

    def info(self, token, msg):
        self.__build(token, "INFO", msg)

    def warning(self, token, msg):
        self.__build(token, "WARNING", msg)

    def error(self, token, msg):
        self.__build(token, "ERROR", msg)

    def critical(self, token, msg):
        self.__build(token, "CRITICAL", msg)