"""Module provides logo and user input functions for STS"""

import logging

logger = logging.getLogger(__name__)


def get_ui_int(message, max_value, min_value=1):
    """function returns an int to user, parameters = "prompt message",
    max value and optional min value (must be > 0)"""

    while True:
        try:
            choice = int(input(message))
            if choice not in range(min_value, max_value + 1):
                raise ValueError(
                    f"Input must be a number between {min_value} - {max_value}"
                )
            print()
            break

        except ValueError as error:
            logger.error(error)
            print(f"\nInput must be a number between {min_value} - {max_value}\n")
    return choice


def get_ui_yn(message):
    """function prompts user for a y/N answer then returns true or false"""

    user_input = {"y": True, "yes": True, "n": False, "no": False}

    while True:
        try:
            choice = input(message).lower().strip()
            print()
            if choice not in ("y", "n", "yes", "no"):
                raise ValueError("input must only be y/N")
            break

        except ValueError as error:
            logger.error(error)
            print(f"{error}\n")

    return user_input[choice]


def get_ui_str(message, max_len=0, min_len=1, alpha=False):
    """function takes a message and prompts user for text input, returning a string"""

    if min_len == 0:
        logger.error("min_len var cannot be 0")
        min_len = 1

    while True:
        try:
            user_text = input(message)
            print()

            if alpha and not user_text.isalpha():
                raise ValueError("Input must only contain letters")

            if max_len and not len(user_text) in range(min_len, max_len + 1):
                if max_len == min_len:
                    raise ValueError(f"Input must be {min_len} characters")
                raise ValueError(
                    f"Input length must be between {min_len} and {max_len} characters"
                )

            if len(user_text) < min_len:
                raise ValueError(f"Input must be at least {min_len} characters")

            break

        except ValueError as error:
            logger.error(error)
            print(f"{error}\n")

    return user_text.strip()
