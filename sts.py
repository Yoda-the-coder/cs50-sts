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

import datetime
import sqlite3

import stsUX
import stsDBOps
import stsTicketOps
from stsTicket import Ticket

database = "sts.db"
global_ticket_count = 0


def create_ticket_2():
    print()
    ticket = stsTicketOps.create_ticket()
    ticket.print_ticket()
    ticket.save_ticket(database, "create")
    print()
    del ticket
    global global_ticket_count
    global_ticket_count = stsDBOps.count_tickets(database)


def update_ticket_2():
    if global_ticket_count == 0:
        print("There are currently no tickets in the database")
    else: 
        ticket_info = stsDBOps.find_ticket(database)
        while ticket_info:
            ticket = Ticket(ticket_info[1], ticket_info[2], ticket_info[3], ticket_info[4], ticket_info[6], ticket_info[8])
            ticket.id = ticket_info[0]
            update_complete = False
            while not update_complete:
                ticket.update_ticket()
                ticket.print_ticket()
                choice = ""
                while not choice.lower() == "y" and not choice.lower() == "n":
                    choice = input("Would you like to update any more fields on the ticket? (y/n): ").lower()
                if choice == "n":                    
                    update_complete = True
                    print()
                    ticket.save_ticket(database, "update")
            ticket_info = False
            del ticket


def view_ticket_2():
    print()
    if global_ticket_count == 0:
        print("There are currently no tickets in the database")
    else: 
        choice = ""
        while not choice.lower() == "y" and not choice.lower() == "n":
            choice = input("Would you like to view all tickets? (y/n): ").lower()
            print()

        if choice == "y":    
            if not stsDBOps.view_all_tickets(database):
                print("No tickets found")
        else:
            stsDBOps.find_ticket(database)


def delete_ticket_2():
    print()
    if global_ticket_count == 0:
        print("There are currently no tickets in the database")
    else: 
        stsDBOps.delete_ticket(database)
        print()
        global_ticket_count = stsDBOps.count_tickets(database)


main_menu_list = [
    create_ticket_2,
    update_ticket_2,
    view_ticket_2,
    delete_ticket_2
]


def main_menu():
    menu_choice = 0
    while not menu_choice == 5:
        stsUX.print_menu()
        menu_choice = stsUX.get_ui_int("Enter your selection (1 - 5): ", 5)
        
        if menu_choice in range(1, 4):
            main_menu_list[menu_choice - 1]()
                        

def main():
    # displays sts logo, name and version
    stsUX.print_logo(__version__)

    # initialise db connection, confirm successful connection test
    stsDBOps.db_init(database)

    # shows user number of tickets in the database
    global global_ticket_count
    global_ticket_count = stsDBOps.count_tickets(database)

    # main menu
    print()
    main_menu()

    # quit STS
    print("\n - Thank you for using - ")
    stsUX.print_logo(__version__)

    return 0
    

if __name__ == "__main__":
    main()