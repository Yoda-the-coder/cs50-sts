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

__version__ = 1.1
__maintainer__ = "ashtaylor2010@gmail.com"
__author__ = "Ashley Taylor"
__status__ = "prototype"
__date__ = "15-02-2008"

import sts_ux
import sts_db_ops
from sts_ticket import Ticket

DATABASE = "sts.db"


def create_ticket():
    """Function prompts user for necessary info
    and returns a 'ticket' obj.
    """
    print()
    ticket_sev = sts_ux.get_ui_int(
        "Please input ticket severity, 1 (high) - 5 (low): ", 5)
    ticket_title = sts_ux.get_ui_str(
        "Please enter a ticket title (max: 30 chars): ", 30, 5)
    if sts_ux.get_ui_yn("Would you like to add any information to the ticket? (y/n): "):
        ticket_info = sts_ux.get_ui_str(
            "Please enter ticket information (max: 100 characters): ", 100)
    else:
        ticket_info = "N/A"
    username = sts_ux.get_ui_str(
        "Please enter your employee ID (8 characters): ", 8, 8)
    # date_created = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ticket = Ticket(ticket_sev, ticket_title, ticket_info, username)

    ticket.print_ticket()
    # TO DO - Move func to db ops module and add date/time
    ticket.save_ticket(DATABASE, "create")
    print()
    del ticket


def update_ticket():
    """Function updates a ticket currently in the db"""
    ticket_count = sts_db_ops.count_tickets(DATABASE)
    if ticket_count == 0:
        print("There are currently no tickets in the database")
    else:
        username = sts_ux.get_ui_str(
        "Please enter your employee ID (8 characters): ", 8, 8)
        ticket_info = sts_db_ops.find_ticket(DATABASE)
        while ticket_info:
            # ************* TO DO ****************
            ticket = Ticket(ticket_info[1], ticket_info[2], ticket_info[4], username)
            ticket.i_d = ticket_info[0]
            update_complete = False
            while not update_complete:
                ticket.update_ticket()
                ticket.print_ticket()
                choice = ""
                while choice.lower() != "y" and choice.lower() != "n":
                    choice = input(
                        "Would you like to update any more fields on the ticket? (y/n): ").lower()
                if choice == "n":
                    update_complete = True
                    print()
                    ticket.save_ticket(DATABASE, "update")
            ticket_info = False
            del ticket


def view_ticket():
    """Function prompts user and either displays all tickets or a selected ticket"""
    print()
    ticket_count = sts_db_ops.count_tickets(DATABASE)
    if ticket_count == 0:
        print("There are currently no tickets in the database")
    else:
        choice = sts_ux.get_ui_yn(
            "Would you like to view all tickets? (y/n): ")
        if choice == "y":
            sts_db_ops.view_all_tickets(DATABASE)
        else:
            sts_db_ops.find_ticket(DATABASE)


def delete_ticket():
    """Function checks for tickets then calls the delete_ticket function from sts_db_ops module"""
    print()
    ticket_count = sts_db_ops.count_tickets(DATABASE)
    if ticket_count == 0:
        print("There are currently no tickets in the database")
    else:
        sts_db_ops.delete_ticket(DATABASE)
        print()


main_menu_list = {
    1: ("Create Ticket", create_ticket),
    2: ("Update a Ticket", update_ticket),
    3: ("View Ticket/s", view_ticket),
    4: ("Delete a Ticket", delete_ticket),
    5: ("Quit Simple-Ticketing-System", None)
}


def print_menu():
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
    menu_choice = 0
    while menu_choice != 5:
        print_menu()
        menu_choice = sts_ux.get_ui_int("Enter your selection (1 - 5): ", 5)

        if menu_choice in range(1, 4):
            main_menu_list[menu_choice][1]()


def main():
    """Main sts function that is first run, looks after startup, main menu and quitting"""
    # displays sts logo, name and version
    sts_ux.print_logo(__version__)

    # initialise db connection, confirm successful connection test
    sts_db_ops.db_init(DATABASE)

    # shows user number of tickets in the database
    sts_db_ops.count_tickets(DATABASE)

    # main menu
    print()
    main_menu()

    # quit STS
    print("\n - Thank you for using - ")
    sts_ux.print_logo(__version__)

    return 0


if __name__ == "__main__":
    main()
