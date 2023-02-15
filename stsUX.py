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