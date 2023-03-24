"""Module provides user input validation methods"""

import logging
from sts_logging import log_function

logger = logging.getLogger(__name__)


@log_function
def get_ui_int(message, max_value, min_value=1):
    """Function returns an int to user, parameters = "prompt message",
    max value and optional min value (must be > 0)"""

    while True:
        choice = int_validation(message, max_value, min_value)
        if choice:
            break

    return choice


@log_function
def int_validation(message, max_value, min_value):
    """Helper function prompts user for int and validates input"""

    try:
        choice = int(input(message))
        if choice not in range(min_value, max_value + 1):
            raise ValueError(
                f"Input must be a number between {min_value} - {max_value}"
            )
        print()
        return choice

    except ValueError as error:
        logger.error(error)
        print(f"\nInput must be a number between {min_value} - {max_value}\n")
        return False


@log_function
def get_ui_yn(message):
    """function prompts user for a y/N answer then returns true or false"""

    user_input = {"y": True, "yes": True, "n": False, "no": False}
    while True:
        choice = yn_validation(message)
        if choice:
            break
    return user_input[choice]


@log_function
def yn_validation(message):
    """Helper function prompts user for y/N before validating and returning input"""

    try:
        choice = input(message).lower().strip()
        if choice not in ("y", "n", "yes", "no"):
            raise ValueError("input must only be y/N")
        print()
        return choice
    except ValueError as error:
        logger.error(error)
        print(f"{error}\n")
        return False


@log_function
def get_ui_str(message, max_len=0, min_len=1, alpha=False, spaces=True):
    """Function displays message to user, prompting for input. A maximum and minimum
    length can be set - prompting the user and retrying until input is valid.
    Function also contains the option to accept only alpha input (non-numeric)
    """

    if min_len == 0:
        logger.error("min_len var cannot be 0")
        min_len = 1

    while True:
        user_input = string_validation(message, max_len, min_len, alpha, spaces)

        if user_input:
            break

    return user_input


@log_function
def string_validation(message, max_len, min_len, alpha, spaces):
    """Helper function validates user input against length and (if selected)
    alphabetical characters only"""

    try:
        user_text = input(message).strip()
        print()
        if (alpha and spaces) and not all(
            x.isalpha() or x.isspace() for x in user_text
        ):
            raise ValueError("Input must only contain letters")
        if (alpha and not spaces) and not user_text.isalpha():
            raise ValueError("Input must only contain letters (no spaces)")

        # Validates input is within range of min <> max lengths
        if max_len and not len(user_text) in range(min_len, max_len + 1):
            if max_len == min_len:
                raise ValueError(f"Input must be {min_len} characters")
            raise ValueError(
                f"Input length must be between {min_len} and {max_len} characters"
            )

        # Validates input against min_length
        if len(user_text) < min_len:
            raise ValueError(f"Input must be at least {min_len} characters")

        return user_text.strip()

    except ValueError as error:
        logger.error(error)
        print(f"{error}\n")
        return False
