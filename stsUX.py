def print_logo(version):
    # function prints STS logo and version to screen
    print(f"""
███████╗████████╗███████╗
██╔════╝╚══██╔══╝██╔════╝
███████╗   ██║   ███████╗
╚════██║   ██║   ╚════██║
███████║   ██║   ███████║
╚══════╝   ╚═╝   ╚══════╝
                         
Simple Ticketing System v{version}
    """)


def print_menu():
    # function prints main menu to screen 
    print(
"""Main Menu:

1: Create Ticket
2: Update a Ticket
3: View Ticket/s
4: Delete a Ticket
5: Quit Simple-Ticket-System
    """)


def get_ui_int(message, max_value, min_value=1):
    error_prompt = f"Choice must be a number between {min_value} - {max_value}"
    choice = 0
    while not choice in range(min_value, max_value + 1):
        try:
            choice = int(input(message))
        except ValueError:
            print(error_prompt)
        else:
            if not choice in range(min_value, max_value + 1):
                print(error_prompt)
    return choice


def get_ui_yn(message):
    error_prompt = "Choice must be either 'y' or 'n'"
    choice = ""
    while not choice == "y" or not choice == "n":
        choice = input(message)
        if not choice == "y" or not choice == "n":
            print(error_prompt)
    return choice


def get_ui_str(message, max_len=0, min_len=1):
    error_prompt = f"Input length must be between {min_len} and {max_len} characters"
    user_text = ""

    if min_len == 0:
        min_len = 1

    while len(user_text) < min_len:
        user_text = input(message)
        if max_len and not len(user_text) in range(min_len, max_len + 1):
            print(error_prompt)
            user_text = ""

    return user_text

