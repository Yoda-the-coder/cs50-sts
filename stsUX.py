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
    user_input = {
        "y": True,
        "n": False
    }
    error_prompt = "Choice must be either 'y' or 'n'"
    choice = ""
    while not choice == "y" and not choice == "n":
        choice = input(message).lower()
        print(choice)
        print(user_input[choice])
        if not choice == "y" and not choice == "n":
            print(error_prompt)
    return user_input[choice]


def get_ui_str(message, max_len=0, min_len=1):
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


def get_ui_ticket_status():
    ticket_status = 0
    statuses = {
        1: "created", 
        2: "awaiting response", 
        3: "in process", 
        4: "closed"}

    print("Please enter a number to select a ticket status from the following options:\n")
    
    for status in statuses:
        print(f"{status}: {statuses[status].capitalize()}")
    print()

    while ticket_status < 1 or ticket_status > 5:
        try:
            ticket_status = int(input(f"Enter number between 1 - {len(statuses)}: "))
        except ValueError:
            print(f"User must enter a number between 1 - {len(statuses)}")
    return statuses[ticket_status]