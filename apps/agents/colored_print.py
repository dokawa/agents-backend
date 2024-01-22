RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"


def print_red(message):
    colored_print(message, RED)


def print_green(message):
    colored_print(message, GREEN)


def print_yellow(message):
    colored_print(message, YELLOW)


def print_blue(message):
    colored_print(message, BLUE)


def print_magenta(message):
    colored_print(message, MAGENTA)


def print_cyan(message):
    colored_print(message, CYAN)


def print_white(message):
    colored_print(message, WHITE)


def colored_print(message, color):
    print(f"{color}{message}{RESET}")
