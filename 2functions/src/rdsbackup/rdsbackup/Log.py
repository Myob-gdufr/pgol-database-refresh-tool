from enum import Enum
import os


class LogLevel(Enum):
    TRACE = 1
    DEBUG = 2
    INFO = 3
    NOTICE = 4
    WARN = 5
    ERROR = 6

    def __str__(self):
        return Enum.__str__(self).split('.')[-1]


class Log:
    def __init__(self, context, log_level=None):
        self.__log_level = self.__get_initial_loglevel(context, log_level)
        self.__context = context

    @property
    def __log_level(self):
        return self.__log_level_value

    @__log_level.setter
    def __log_level(self, value):
        self.__log_level_value = value

    @property
    def __context(self):
        return self.__context_value

    @__context.setter
    def __context(self, value):
        self.__context_value = value

    @classmethod
    def __get_initial_loglevel(cls, context, log_level):
        #  Log level setting priorities:
        #    1. Explicit setting in the log constructor
        #    2. Explicit setting in the environment variable PGOL_LOG_{context}
        #    3. Log setting in the default context
        if log_level is not None:
            return log_level

        environ_log_level = os.environ.get("PGOL_LOG_{context}".format(context=context))
        if environ_log_level is not None:
            return environ_log_level

        #  Hard code it as NOTICE for now.
        return LogLevel.NOTICE

    def log(self, log_id, level, message, params):
        if level.value < self.__log_level.value:
            # below the logging level.
            return
        print("[{log_id}] [{loglevel}] {message}".format(
            log_id=log_id,
            loglevel=str(level),
            message=message.format(**params)
        ))

    def trace(self, log_id, message, params):
        self.log(log_id, LogLevel.TRACE, message, params)

    def debug(self, log_id, message, params):
        self.log(log_id, LogLevel.DEBUG, message, params)

    def info(self, log_id, message, params):
        self.log(log_id, LogLevel.INFO, message, params)

    def notice(self, log_id, message, params):
        self.log(log_id, LogLevel.NOTICE, message, params)

    def warn(self, log_id, message, params):
        self.log(log_id, LogLevel.WARN, message, params)

    def error(self, log_id, message, params):
        self.log(log_id, LogLevel.ERROR, message, params)


GlobalLog = Log("global")


def log(log_level, message_format, params):
    GlobalLog.log("ZZZ000", log_level, message_format, **params)


def trace(message_format, params):
    log(LogLevel.TRACE, message_format, params)


def debug(message_format, params):
    log(LogLevel.DEBUG, message_format, params)


def info(message_format, params):
    log(LogLevel.INFO, message_format, params)


def notice(message_format, params):
    log(LogLevel.NOTICE, message_format, params)


def warn(message_format, params):
    log(LogLevel.WARN, message_format, params)


def error(message_format, params):
    log(LogLevel.ERROR, message_format, params)
