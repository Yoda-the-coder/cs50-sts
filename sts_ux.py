"""Module provides logo and user input functions for STS"""


def print_logo(version):
    """function prints STS logo and version to screen"""

    print(f"""
███████╗████████╗███████╗
██╔════╝╚══██╔══╝██╔════╝
███████╗   ██║   ███████╗
╚════██║   ██║   ╚════██║
███████║   ██║   ███████║
╚══════╝   ╚═╝   ╚══════╝
                         
Simple Ticketing System v{version}
    """)


def get_ui_int(message, max_value, min_value=1):
    """function returns an int to user, parameters = "prompt message", 
    max value and optional min value (must be > 0)"""
    error_prompt = f"Choice must be a number between {min_value} - {max_value}"
    choice = 0
    while choice not in range(min_value, max_value + 1):
        try:
            choice = int(input(message))
        except ValueError:
            print(error_prompt)
        else:
            if choice not in range(min_value, max_value + 1):
                print(error_prompt)
    return choice


def get_ui_yn(message):
    """function returns prompts user for a y/n answer then returns true or false"""
    user_input = {
        "y": True,
        "n": False
    }
    error_prompt = "Choice must be either 'y' or 'n'"
    choice = ""
    while choice not in ("y", "n"):
        choice = input(message).lower().strip()
        if choice not in ("y", "n"):
            print(error_prompt)
    return user_input[choice]


def get_ui_str(message, max_len=0, min_len=1):
    """function takes a message and prompts user for text input, returning a string"""
    error_prompt = f"Input length must be between {min_len} and {max_len} characters"
    user_text = ""

    if min_len == 0:
        min_len = 1

    while len(user_text) < min_len:
        user_text = input(message)
        if max_len and not len(user_text) in range(min_len, max_len + 1):
            if max_len == min_len:
                print(f"Input must be {min_len} characters")
            else:
                print(error_prompt)
            user_text = ""
    return user_text
