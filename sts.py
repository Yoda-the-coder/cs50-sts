"""STS - Simple-Ticketing-System.

Usage: sts.py
Firstly the DATABASE_INFO is checked and a main menu is displayed, offering
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

import sys
import logging
from datetime import datetime
import sts_user_inputs
import sts_db_ops
from sts_ticket import Ticket
from sts_logging import log_function


DATABASE_INFO = {"db_name": "./database/test_sts_database.db", "table_name": "tickets"}

# inits log file and logging settings
logging.basicConfig(
    format="%(asctime)s %(levelname)s :: %(name)s :: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f'./logs/{datetime.now().strftime("%Y-%m-%d %H:%M")}_sts_log.log',
    filemode="w",
    encoding="utf-8",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# CREATE
@log_function
def create_ticket(username):
    """Function prompts user for necessary info
    and returns a 'ticket' obj.
    """

    ticket_sev = sts_user_inputs.get_ui_int(
        "Please input ticket severity, 1 (high) - 5 (low): ", 5
    )

    ticket_title = sts_user_inputs.get_ui_str(
        "Please enter a ticket title (max: 30 chars): ", 30, 5
    )

    if sts_user_inputs.get_ui_yn(
        "Would you like to add any information to the ticket? (y/N): "
    ):
        ticket_info = sts_user_inputs.get_ui_str(
            "Please enter ticket information (max: 100 characters): ", 100
        )
    else:
        ticket_info = "N/A"

    # date_created = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ticket = Ticket(ticket_sev, ticket_title, ticket_info, username)
    logger.info("new ticket created by '%s'", username)

    ticket.print_ticket()

    if not sts_user_inputs.get_ui_yn("Would you like to save the ticket? (y/N): "):
        if sts_user_inputs.get_ui_yn(
            "Are you sure you would like to delete the ticket? (y/N): "
        ):
            logger.warning("ticket not saved to db")
            return

    sts_db_ops.insert_ticket_to_db(DATABASE_INFO, ticket)

    del ticket


# READ
@log_function
def view_tickets(username):
    """Function dynamically prints the view menu options,
    gets UI and launches relevant view function.
    """

    if not sts_db_ops.count_tickets(DATABASE_INFO):
        return False

    while True:
        return view_tickets_menu(username)


# UPDATE
@log_function
def update_ticket(username):
    """Function finds and updates a ticket in the db"""

    # Checks whether db contains any tickets, returns to main menu if False
    if not sts_db_ops.count_tickets(DATABASE_INFO):
        return False

    # Find ticket ID
    if not find_ticket_id(username):
        return False

    # Queries db by ID and returns a ticket object to be updated
    ticket_search_result = search_db_by_id()
    try:
        ticket = Ticket(
            ticket_search_result[0][1],
            ticket_search_result[0][2],
            ticket_search_result[0][4],
            username,
        )
        ticket.i_d = ticket_search_result[0][0]
    except TypeError as error:
        logger.error("%s - id not in database", error)
        return False

    # Updates ticket object
    while True:
        print_update_menu()
        menu_choice = sts_user_inputs.get_ui_int(
            f"Enter your selection (1 - {len(update_ticket_list)}): ",
            len(update_ticket_list),
        )
        logger.info("%s - '%s'", update_ticket_list[menu_choice][0], username)

        if menu_choice == 5:
            return False

        ticket = update_ticket_list[menu_choice][1](ticket)

        if not sts_user_inputs.get_ui_yn(
            "Would you like to update any more fields? (y/N): "
        ):
            ticket.print_ticket()
            break

    # user confirms save changes, if no - process quit
    if not sts_user_inputs.get_ui_yn("Would you like to save updates? (y/n): "):
        if sts_user_inputs.get_ui_yn("Are you sure? All updates will be lost! (y/n): "):
            logger.warning("user cancelled update - ticket not saved to db")
            del ticket
            return False

    # Updates ticket in DATABASE_INFO, prints confirmation message if successful
    sts_db_ops.update_ticket_to_db(DATABASE_INFO, ticket)
    return True


# DELETE
@log_function
def delete_ticket(username):
    """Function checks for tickets then calls the delete_ticket function from sts_db_ops module"""

    if not sts_db_ops.count_tickets(DATABASE_INFO):
        return False

    # Find ticket ID
    if not find_ticket_id(username):
        return False

    # Gets ticket by ID
    ticket = search_db_by_id()

    # Queries user before attempting to delete ticket from db
    try:
        if ticket and sts_user_inputs.get_ui_yn(
            "Would you like to delete the ticket? (y/N): "
        ):
            if sts_user_inputs.get_ui_yn(
                "Are you sure? The ticket will be lost forever! (y/N): "
            ):
                sts_db_ops.delete_ticket_by_id(DATABASE_INFO, ticket[0][0])
                return True

        logger.info("user cancelled ticket deletion")
        print("The ticket has not been deleted\n")
        return False

    except TypeError as error:
        logger.error("%s - id not in database", error)
        print("Ticket ID not found in database\n")
        return False


@log_function
def find_ticket_id(username):
    """Function to assist user find ticket id"""

    while True:
        if sts_user_inputs.get_ui_yn("Do you know the ticket ID? (y/N): "):
            break

        if not view_tickets_menu(username):
            return False

    return True


@log_function
def update_severity(ticket):
    """Function updates the severity of a ticket and returns updated ticket object"""

    ticket.sev = sts_user_inputs.get_ui_int(
        "Please input ticket severity, 1 (high) - 5 (low): ", 5
    )
    return ticket


@log_function
def update_title(ticket):
    """Function updates the title of a ticket and returns updated ticket object"""

    ticket.title = sts_user_inputs.get_ui_str("Please enter the updated title: ", 30)
    return ticket


@log_function
def update_status(ticket):
    """Function updates the status of a ticket and returns updated ticket object"""

    print_ticket_statuses()

    status_index = sts_user_inputs.get_ui_int(
        f"Select a status from the above options (1 - {len(ticket_statuses_list)}): ",
        len(ticket_statuses_list),
    )

    ticket.status = ticket_statuses_list[status_index - 1]
    return ticket


@log_function
def update_info(ticket):
    """Function updates the info of a ticket and returns updated ticket object"""

    ticket.info = sts_user_inputs.get_ui_str(
        "Please enter updated ticket information (max: 100 characters): ", 100
    )
    return ticket


@log_function
def search_db_by_id():
    """Prompts user for ID, prints ticket to screen or notifies user ticket doesn't exist"""
    min_max_ids = sts_db_ops.find_id_range(DATABASE_INFO)
    ticket_id = sts_user_inputs.get_ui_int(
        "Please enter the ticket ID: ", int(min_max_ids[0][1]), int(min_max_ids[0][0])
    )

    ticket = sts_db_ops.search_database(DATABASE_INFO, "id", ticket_id)
    if not ticket:
        print("Ticket ID not found in Database\n")
        return False
    return ticket


@log_function
def search_db_by_title():
    """Prompts user for title, prints ticket to screen or notifies user ticket doesn't exist"""
    ticket_title = sts_user_inputs.get_ui_str("Please enter the title to search: ", 30)
    search = f"%{ticket_title}%"

    if not sts_db_ops.search_database(DATABASE_INFO, "title", search, "title"):
        print("No match found in the database\n")


@log_function
def search_db_by_sev():
    """Prompts user for info, prints ticket to screen or notifies user if ticket doesn't exist"""
    search = sts_user_inputs.get_ui_int(
        "Please input ticket severity, 1 (high) - 5 (low): ", 5
    )

    if not sts_db_ops.search_database(DATABASE_INFO, "severity", search, "severity"):
        print("No match found in the database\n")


@log_function
def search_db_by_status():
    """prompts user for ticket status, queries db and prints results to screen"""
    print_ticket_statuses()

    search = sts_user_inputs.get_ui_int(
        f"Select a status from the above options (1 - {len(ticket_statuses_list)}): ",
        len(ticket_statuses_list),
    )

    if not sts_db_ops.search_database(
        DATABASE_INFO, "status", ticket_statuses_list[search - 1], "status"
    ):
        print("No match found in the database\n")


@log_function
def search_db_by_username():
    """Prompts user for a username, queries db and prints results to screen"""
    username = "0"
    while not username.isalpha():
        username = sts_user_inputs.get_ui_str(
            "Please enter employee ID to search (8 characters): ", 8, 8
        )
        if not username.isalpha():
            print("User name can only contain letters\n")

    if not sts_db_ops.search_database(DATABASE_INFO, "username", username):
        print("No match found in the database\n")


@log_function
def get_username():
    """function queries user, validates and returns username"""

    username = "0"
    username_2 = "1"
    while True:
        try:
            username = sts_user_inputs.get_ui_str(
                "Please enter employee ID (8 characters): ", 8, 8, True, False
            )

            username_2 = sts_user_inputs.get_ui_str(
                "Please re-enter employee ID: ", 8, 8, True, False
            )

            if username != username_2:
                raise ValueError("Usernames do not match, please retry")

            break

        except ValueError as error:
            logger.error(error)
            print(f"{error}\n")

    return username


@log_function
def view_tickets_menu(username):
    """prints view menu and calls appropriate function to view by user selection"""

    menu_size = len(view_ticket_list)
    menu_choice = 0

    print_view_menu(menu_size)
    menu_choice = sts_user_inputs.get_ui_int(
        f"Enter your selection (1 - {menu_size}): ", menu_size
    )
    logger.info("%s - '%s'", view_ticket_list[menu_choice][0], username)

    if menu_choice == 1:
        view_ticket_list[menu_choice][1](DATABASE_INFO)
        return True

    if menu_choice in range(2, menu_size):
        view_ticket_list[menu_choice][1]()
        return True

    return False


@log_function
def print_update_menu():
    """function prints update ticket options to screen"""

    logger.info("update ticket menu displayed")
    print("--- Update Ticket ---\n")
    for i in range(1, len(update_ticket_list) + 1):
        print(f"{i}: {update_ticket_list[i][0]}")
    print()


@log_function
def print_view_menu(menu_length):
    """Function prints view menu list to screen"""

    logger.info("view ticket/s menu displayed")
    print("--- View Menu ---\n")
    for i in range(1, menu_length + 1):
        print(f"{i}: {view_ticket_list[i][0]}")
    print()


@log_function
def print_ticket_statuses():
    """function prints ticket status options to screen"""

    logger.info("ticket status options displayed")
    print("--- Ticket Statuses ---\n")
    for count, value in enumerate(ticket_statuses_list):
        print(f"{count + 1}: {value.capitalize()}")
    print()


@log_function
def print_main_menu():
    """function prints main menu to screen"""

    logger.info("main menu displayed")
    print("--- Main menu ---\n")
    for i in range(1, len(main_menu_list) + 1):
        print(f"{i}: {main_menu_list[i][0]}")
    print()


@log_function
def print_logo(version):
    """function prints STS logo and version to screen"""

    print(
        f"""
███████╗████████╗███████╗
██╔════╝╚══██╔══╝██╔════╝
███████╗   ██║   ███████╗
╚════██║   ██║   ╚════██║
███████║   ██║   ███████║
╚══════╝   ╚═╝   ╚══════╝
                         
Simple Ticketing System v{version}
    """
    )


@log_function
def main_menu():
    """Function dynamically prints the menu options,
    gets UI and launches relevant function. If user
    inputs '6', program will quit.
    """

    # prints menu to screen, prompts user, calls appropriate method
    menu_choice = 5
    while menu_choice != 6:
        # sets username
        if menu_choice == 5:
            username = get_username()
            logger.info("logged in as '%s'", username)
            print(f"You are logged in as: '{username}'\n")

        print_main_menu()

        # prompts user for menu choice
        menu_choice = sts_user_inputs.get_ui_int("Enter your selection (1 - 6): ", 6)

        # calls appropriate func dependent on user input
        if menu_choice in range(1, len(main_menu_list) - 1):
            logger.info("main menu - %s", main_menu_list[menu_choice][0])
            main_menu_list[menu_choice][1](username)


@log_function
def main():
    """Main sts function that is first run, looks after startup, main menu and quitting"""

    logger.info("application started")

    # displays sts logo, name and version
    print_logo(__version__)

    # initialise db connection, confirm successful connection test
    if not sts_db_ops.db_test(DATABASE_INFO):
        print("Terminating due to error connecting to database - see logs")
        logger.error("error connecting to database")
        sys.exit(1)

    # shows user number of tickets in the database
    if sts_db_ops.count_tickets(DATABASE_INFO) is False:
        print("Error counting tickets, see logs.")

    # main menu
    main_menu()

    # quit STS
    print(" - Thank you for using - ")
    print_logo(__version__)

    logger.info("application finished")
    sys.exit(0)


update_ticket_list = {
    1: ("Update Ticket Severity", update_severity),
    2: ("Update Ticket Title", update_title),
    3: ("Update Ticket Status", update_status),
    4: ("Update Ticket Information", update_info),
    5: ("Return to Main Menu", None),
}


ticket_statuses_list = ["Created", "Awaiting Response", "In Process", "Closed"]


view_ticket_list = {
    1: ("View All Tickets", sts_db_ops.view_all_tickets),
    2: ("Search Tickets by ID", search_db_by_id),
    3: ("Search Tickets by Title", search_db_by_title),
    4: ("Search Tickets by Severity", search_db_by_sev),
    5: ("Search Tickets by Status", search_db_by_status),
    6: ("Search Tickets by Username", search_db_by_username),
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
