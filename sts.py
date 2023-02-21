"""STS - Simple-Ticketing-System.

Usage: sts.py
Firstly the database is checked and a main menu is displayed, offering
capabilities to create, read, update, delete and store departmental
IT tickets.
Target users: Department engineers and managers.
Target system: OSX
Interface: Command-line
Functional requirements:
Testing methods:
Expected results:
Limitations: 
"""

__version__ = 2.0
__maintainer__ = "ashtaylor2010@gmail.com"
__author__ = "Ashley Taylor"
__status__ = "prototype"
__date__ = "15-02-2008"

import sts_ux
import sts_db_ops
from sts_ticket import Ticket

DATABASE = "sts_database.db"


# CREATE
def create_ticket(username):
    """Function prompts user for necessary info
    and returns a 'ticket' obj.
    """
    print()
    ticket_sev = sts_ux.get_ui_int(
        "Please input ticket severity, 1 (high) - 5 (low): ", 5
    )
    print()
    ticket_title = sts_ux.get_ui_str(
        "Please enter a ticket title (max: 30 chars): ", 30, 5
    )
    print()
    if sts_ux.get_ui_yn("Would you like to add any information to the ticket? (y/n): "):
        print()
        ticket_info = sts_ux.get_ui_str(
            "Please enter ticket information (max: 100 characters): ", 100
        )
    else:
        ticket_info = "N/A"

    # date_created = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ticket = Ticket(ticket_sev, ticket_title, ticket_info, username)

    ticket.print_ticket()

    if not sts_ux.get_ui_yn("Would you like to save the ticket? (y/n): "):
        print()

        if sts_ux.get_ui_yn(
            "Are you sure you would like to delete the ticket? (y/n): "
        ):
            print()
            return

    print()
    sts_db_ops.insert_ticket_to_db(DATABASE, ticket)

    print()
    del ticket


# READ
def view_tickets(username):
    """Function dynamically prints the view menu options,
    gets UI and launches relevant view function.
    """
    print()
    if not sts_db_ops.count_tickets(DATABASE):
        return
    print()
    menu_size = len(view_ticket_list)
    menu_choice = 0
    while menu_choice != len(view_ticket_list):
        print_view_menu(len(view_ticket_list))
        menu_choice = sts_ux.get_ui_int(
            f"Enter your selection (1 - {menu_size}): ", menu_size
        )
        print()
        if menu_choice == 1:
            view_ticket_list[menu_choice][1](DATABASE)
            print(f"Database accessed by {username}")
            print()
            # TO DO - log all tickets viewed by username, datetime
        elif menu_choice in range(2, menu_size):
            view_ticket_list[menu_choice][1]()


# UPDATE
def update_ticket(username):
    """Function updates a ticket currently in the db"""
    print()
    if not sts_db_ops.count_tickets(DATABASE):
        return
    print()

    # ID check / find ticket ID path
    id_known = False
    while not id_known:
        id_known = sts_ux.get_ui_yn("Do you know the ticket ID? (y/n): ")
        print()
        if id_known:
            break

        menu_size = len(view_ticket_list) - 1
        menu_choice = 0

        print_view_menu(menu_size)
        menu_choice = sts_ux.get_ui_int(
            f"Enter your selection (1 - {menu_size}): ", menu_size
        )
        print()
        if menu_choice == 1:
            view_ticket_list[menu_choice][1](DATABASE)
            print(f"Database accessed by {username}")
        elif menu_choice in range(2, menu_size + 1):
            view_ticket_list[menu_choice][1]()

    # Gets ticket by ID and creates a ticket object to be updated
    ticket_list = search_by_id()
    ticket = Ticket(ticket_list[0][1], ticket_list[0][2], ticket_list[0][4], username)
    ticket.i_d = ticket_list[0][0]

    # Updates ticket object
    update_flag = True
    while update_flag:
        print_update_menu()
        menu_choice = sts_ux.get_ui_int(
            f"Enter your selection (1 - {len(update_ticket_list)}): ",
            len(update_ticket_list),
        )

        ticket = update_ticket_list[menu_choice][1](ticket)
        print()
        update_flag = sts_ux.get_ui_yn(
            "Would you like to update anymore fields? (y/n): "
        )
        print()
    ticket.print_ticket()

    if not sts_ux.get_ui_yn("Would you like to save updates? (y/n): "):
        print()
        if sts_ux.get_ui_yn("Are you sure? All updates will be lost! (y/n): "):
            return
    print()

    # Updates ticket in database, prints confirmation message if successful
    sts_db_ops.update_ticket_to_db(DATABASE, ticket)
    return


# DELETE
def delete_ticket(username):
    """Function checks for tickets then calls the delete_ticket function from sts_db_ops module"""
    print()
    if not sts_db_ops.count_tickets(DATABASE):
        return
    print()

    # ID check / find ticket ID path
    id_known = False
    while not id_known:
        id_known = sts_ux.get_ui_yn("Do you know the ticket ID? (y/n): ")
        print()
        if id_known:
            break

        menu_size = len(view_ticket_list) - 1
        menu_choice = 0

        print_view_menu(menu_size)
        menu_choice = sts_ux.get_ui_int(
            f"Enter your selection (1 - {menu_size}): ", menu_size
        )
        print()
        if menu_choice == 1:
            view_ticket_list[menu_choice][1](DATABASE)
            print(f"Database accessed by {username}")
        elif menu_choice in range(2, menu_size + 1):
            view_ticket_list[menu_choice][1]()

    # Gets ticket by ID
    ticket_list = search_by_id()

    #  Confirm deletion
    if sts_ux.get_ui_yn("Would you like to delete the ticket? (y/n): "):
        print()
        if not sts_ux.get_ui_yn(
            "Are you sure? The ticket will be lost forever! (y/n): "
        ):
            print()
            return

    # Ticket is permanently deleted from the database
    sts_db_ops.delete_ticket_by_id(DATABASE, ticket_list[0][0])
    return


def update_severity(ticket):
    """Function updates the severity of a ticket and returns updated ticket object"""
    print()
    ticket.sev = sts_ux.get_ui_int(
        "Please input ticket severity, 1 (high) - 5 (low): ", 5
    )
    return ticket


def update_title(ticket):
    """Function updates the title of a ticket and returns updated ticket object"""
    print()
    ticket.title = sts_ux.get_ui_str("Please enter the updated title: ", 30)
    return ticket


def update_status(ticket):
    """Function updates the status of a ticket and returns updated ticket object"""
    print()
    print_ticket_statuses()

    status_index = sts_ux.get_ui_int(
        f"Select a status from the above options (1 - {len(ticket_statuses_list)}): ",
        len(ticket_statuses_list),
    )

    ticket.status = ticket_statuses_list[status_index - 1]
    return ticket


def update_info(ticket):
    """Function updates the info of a ticket and returns updated ticket object"""
    print()
    ticket.info = sts_ux.get_ui_str(
        "Please enter updated ticket information (max: 100 characters): ", 100
    )
    return ticket


def search_by_id():
    """Prompts user for ID, prints ticket to screen or notifies user ticket doesn't exist"""
    min_max_ids = sts_db_ops.find_id_range(DATABASE)
    ticket_id = sts_ux.get_ui_int(
        "Please enter the ticket ID: ", int(min_max_ids[0][1]), int(min_max_ids[0][0])
    )
    print()
    ticket = sts_db_ops.search_database(DATABASE, "id", ticket_id)
    if not ticket:
        print("Ticket ID doesn't exist in database, double check ID")
        return False
    return ticket


def search_by_title():
    """Prompts user for title, prints ticket to screen or notifies user ticket doesn't exist"""
    ticket_title = sts_ux.get_ui_str("Please enter the title to search: ", 30)
    search = f"%{ticket_title}%"
    print()
    if not sts_db_ops.search_database(DATABASE, "title", search, "title"):
        print("No match found in the database")
        print()


def search_by_sev():
    """Prompts user for info, prints ticket to screen or notifies user if ticket doesn't exist"""
    search = sts_ux.get_ui_int("Please input ticket severity, 1 (high) - 5 (low): ", 5)
    print()
    if not sts_db_ops.search_database(DATABASE, "severity", search, "severity"):
        print("No match found in the database")
        print()


def search_by_status():
    """prompts user for ticket status, queries db and prints results to screen"""
    print_ticket_statuses()

    search = sts_ux.get_ui_int(
        f"Select a status from the above options (1 - {len(ticket_statuses_list)}): ",
        len(ticket_statuses_list),
    )
    print()
    if not sts_db_ops.search_database(
        DATABASE, "status", ticket_statuses_list[search - 1], "status"
    ):
        print("No match found in the database")
        print()


def search_by_username():
    """Prompts user for a username, queries db and prints results to screen"""
    username = "0"
    while not username.isalpha():
        username = sts_ux.get_ui_str(
            "Please enter employee ID to search (8 characters): ", 8, 8
        )
        if not username.isalpha():
            print("User name can only contain letters")
    print()

    if not sts_db_ops.search_database(DATABASE, "username", username):
        print("No match found in the database")
        print()


def print_update_menu():
    """function prints update ticket options to screen"""
    print("--- Update Ticket ---\n")
    for i in range(1, len(update_ticket_list) + 1):
        print(f"{i}: {update_ticket_list[i][0]}")
    print()


def print_view_menu(menu_length):
    """Function prints view menu list to screen"""
    print("--- View Menu ---\n")
    for i in range(1, menu_length + 1):
        print(f"{i}: {view_ticket_list[i][0]}")
    print()


def print_ticket_statuses():
    """function prints ticket status options to screen"""
    print("--- Ticket Statuses ---\n")
    for count, value in enumerate(ticket_statuses_list):
        print(f"{count + 1}: {value.capitalize()}")
    print()


def print_main_menu():
    """function prints main menu to screen"""
    print("--- Main menu ---\n")
    for i in range(1, len(main_menu_list) + 1):
        print(f"{i}: {main_menu_list[i][0]}")
    print()


def main_menu():
    """Function dynamically prints the menu options,
    gets UI and launches relevant function. If user
    inputs '5', program will quit.
    """
    menu_choice = 5
    while menu_choice != 6:
        if menu_choice == 5:
            # prompt user for employee id - TO DO: make alpha only.
            username = "0"
            while not username.isalpha():
                print()
                username = sts_ux.get_ui_str(
                    "Please enter employee ID (8 characters): ", 8, 8
                )
                if not username.isalpha():
                    print("User name can only contain letters")

        print()
        print_main_menu()

        menu_choice = sts_ux.get_ui_int("Enter your selection (1 - 6): ", 6)

        if menu_choice in range(1, len(main_menu_list) - 1):
            main_menu_list[menu_choice][1](username)


def main():
    """Main sts function that is first run, looks after startup, main menu and quitting"""
    # displays sts logo, name and version
    sts_ux.print_logo(__version__)

    # initialise db connection, confirm successful connection test
    sts_db_ops.db_init(DATABASE)

    # shows user number of tickets in the database
    sts_db_ops.count_tickets(DATABASE)

    # main menu
    main_menu()

    # quit STS
    print("\n - Thank you for using - ")
    sts_ux.print_logo(__version__)

    return 0


update_ticket_list = {
    1: ("Update Ticket Severity", update_severity),
    2: ("Update Ticket Title", update_title),
    3: ("Update Ticket Status", update_status),
    4: ("Update Ticket Information", update_info),
}


ticket_statuses_list = ["Created", "Awaiting Response", "In Process", "Closed"]


view_ticket_list = {
    1: ("View All Tickets", sts_db_ops.view_all_tickets),
    2: ("Search Tickets by ID", search_by_id),
    3: ("Search Tickets by Title", search_by_title),
    4: ("Search Tickets by Severity", search_by_sev),
    5: ("Search Tickets by Status", search_by_status),
    6: ("Search Tickets by Username", search_by_username),
    7: ("Back to Main Menu", None),
}


main_menu_list = {
    1: ("Create Ticket", create_ticket),
    2: ("Update a Ticket", update_ticket),
    3: ("View Ticket/s", view_tickets),
    4: ("Delete a Ticket", delete_ticket),
    5: ("Change User", None),
    6: ("Quit Simple-Ticketing-System", None),
}


if __name__ == "__main__":
    main()
