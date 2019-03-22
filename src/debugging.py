import time
from utils import *


def format_type(padding, body):
    s = " [" + body + "]"
    return s.ljust(padding, " ")


def format_prefix(padding, body):
    s = body + ":"
    return s.ljust(padding, " ")


def print_message(message, type_prefix, message_type):
    verbosity = config_get_user_verbosity()

    if message_type == "info":
        print(str(time.strftime("%c")) + format_type(12, "INFO") + format_prefix(12, type_prefix) + message)
    elif message_type == "error":
        print(str(time.strftime("%c")) + format_type(12, "ERROR") + format_prefix(12, type_prefix) + message)
    elif message_type == "debug" and verbosity["debug"]:
        print(str(time.strftime("%c")) + format_type(12, "DEBUG") + format_prefix(12, type_prefix) + message)
    elif message_type == "verbose" and verbosity["verbose"]:
        print(str(time.strftime("%c")) + format_type(12, "VERBOSE") + format_prefix(12, type_prefix) + message)
    else:
        print(str(time.strftime("%c")) + format_type(12, "ERROR") + format_prefix(12, type_prefix) + "Unknown type argument supplied to print_message")

