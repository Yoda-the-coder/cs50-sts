"""
Module provides numerous functions to be called by STS for 'ticket' operations.
"""


def get_ticket_sev():
    """prompts user for ticket sev - must be an int between 1 - 5"""
    ticket_sev = 0
    while ticket_sev > 5 or ticket_sev < 1:
        try:
            ticket_sev = int(
                input("Please input ticket severity, 1 (high) - 5 (low): "))
        except ValueError:
            print("User must input a number (1 - 5)")
    return ticket_sev


def get_ticket_title():
    """prompts user for ticket title, must be no greater than 15 chars"""
    ticket_title = ""
    while len(ticket_title) > 30 or len(ticket_title) < 3:
        ticket_title = input("Please enter a ticket title (max: 30 chars): ")
    return ticket_title


def get_ticket_status():
    """prompts user for ticket status"""
    ticket_status = 0
    statuses = {
        1: "created",
        2: "awaiting response",
        3: "in process",
        4: "closed"}

    print("Please enter a number to select a ticket status from the following options:\n")

    for count, value in enumerate(statuses):
        print(f"{count + 1}: {value.capitalize()}")
    print("")

    while ticket_status < 1 or ticket_status > 5:
        try:
            ticket_status = int(
                input(f"Enter number between 1 - {len(statuses)}: "))
        except ValueError:
            print(f"User must enter a number between 1 - {len(statuses)}")
    return statuses[ticket_status]


def get_ticket_info(add_info="x"):
    """prompts user for ticket info"""
    ticket_info = "N/A"

    while add_info.lower() != "y" and add_info.lower() != "n":
        add_info = input(
            "Would you like to add any information to the ticket? (y/n): ").lower()

    if add_info == "n":
        return ticket_info

    while len(ticket_info) < 5 or len(ticket_info) > 100:
        ticket_info = input(
            "Please enter ticket information (max: 100 characters): ")
    return ticket_info


def get_user():
    """prompts user for username"""
    user_name = ""
    while len(user_name) != 8 or not user_name.isalpha():
        user_name = str(input("Please enter employee ID: ")).lower()
    return user_name
