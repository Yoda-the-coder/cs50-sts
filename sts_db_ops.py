"""Module defines functions that interface the sqlite3 database"""

import sqlite3
import datetime
from tabulate import tabulate

import sts_ticket_ops
import sts_ux



def db_error(error):
    """Function prints database error code when sqlite3 error raised"""
    print(f"Error connecting to database: {error} ")
    # log error


def db_init(database):
    """Initialise database by testing connection and returning sqlite version"""
    try:
        db_connection = sqlite3.connect(database)
        cursor = db_connection.cursor()
        print(f"Successfully connected to STS database: {database}")
        db_init_query = "SELECT sqlite_version();"
        cursor.execute(db_init_query)
        db_version = cursor.fetchall()
        cursor.close()
        print(f"SQLite Database version: {db_version[0][0]}")
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
            print("Database connection test completed successfully")
            print()


def prompt_for_id():
    """Prompts user for ticket id, TO BE REMOVED"""
    choice = ""
    while choice not in ('y', 'n'):
        choice = input("Do you know the Ticket ID? (y/n): ").strip().lower()
    return choice


def ticket_view_options():
    """Function prints different view options for user"""
    print(
        """
1: View all tickets
2: Search by 'Username'
3: Search by 'Severity'
4: Search by 'title'
5: Return to Main Menu
"""
    )
    choice = 0
    while choice < 1 or choice > 5:
        try:
            choice = int(input("Enter number between 1 - 4: "))
        except ValueError:
            print("User must enter a number between 1 - 4")
    return choice


def choose_ticket_view(database, choice):
    """Function initiates necessary view function dependent on user's choice"""
    match choice:
        case 1:
            # view all tickets
            print()
            if not view_all_tickets(database):
                print("No tickets found")

        case 2:
            # search by username
            print()
            username = sts_ticket_ops.get_user()
            print()
            if not view_by_user(database, username):
                print("No tickets found")

        case 3:
            # search by severity
            print()
            severity = sts_ticket_ops.get_ticket_sev()
            print()
            if not view_by_severity(database, str(severity)):
                print("No tickets found")

        case 4:
            # search by title
            print()
            title = sts_ticket_ops.get_ticket_title().strip()
            print()
            if not view_by_title(database, title):
                print("No tickets found")


def count_tickets(database):
    """Function counts tickets in db and returns an int"""
    try:
        db_connection = sqlite3.connect(database)
        cursor = db_connection.cursor()
        db_init_query = "SELECT COUNT(*) FROM tickets;"
        cursor.execute(db_init_query)
        tickets_amount = cursor.fetchone()
        cursor.close()
        print(
            f"There are currently {tickets_amount[0]} tickets stored in the STS database")
    except sqlite3.Error as error:
        db_error(error)
        raise sqlite3.Error("Error Reading Database")

    if db_connection:
        db_connection.close()
    return tickets_amount[0]


def insert_ticket_to_db(database, ticket):
    """Function inserts a new ticket into the database"""
    query = """INSERT INTO tickets (severity,title,status,info,updated_by,created_by,
    date_updated,date_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        datetime_created = str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(query, (ticket.sev, ticket.title, ticket.status,
                               ticket.info, ticket.updated_by, ticket.created_by,
                               datetime_created, datetime_created))
        db_connection.commit()  # persists changes to the db
        print("Ticket successfully saved into database")
        cursor.close()  # closes db cursor object
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()


def find_ticket_by_id(database):
    """Searches database for ticket id, if exists, returns the row"""
    query = "SELECT MIN(id), MAX(id) FROM tickets"
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        cursor.execute(query)
        min_max_ids = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()

    ticket_id = sts_ux.get_ui_int("Please enter the ticket ID: ", int(
        min_max_ids[0][1]), int(min_max_ids[0][0]))

    if view_by_id(database, ticket_id):
        return return_ticket(database, ticket_id)

    print("Ticket ID doesn't exist in database, double check ID")
    print()
    return find_ticket(database)


def view_by_id(database, ticket_id):
    """Queries database for ticket matching submitted id"""
    query = "SELECT * FROM tickets WHERE id = ? ORDER BY severity"
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        cursor.execute(query, (ticket_id,))
        ticket = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
    if ticket:
        print(tabulate(ticket, headers=["ID", "Severity", "Title", "Status", "Info", "Updated by",
              "Created by", "Date Updated", "Date Created"],
                       tablefmt="fancy_grid", maxcolwidths=25))
        print()
        return True
    return False


def view_all_tickets(database):
    """Function displays all tickets in database"""
    query = "SELECT * FROM tickets;"
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        cursor.execute(query)
        tickets = cursor.fetchall()
        cursor.close()
        if tickets:
            print(tabulate(tickets, headers=["ID", "Sev", "Title", "Status", "Info", "Updated by",
                                             "Created by", "Date Updated", "Date Created"],
                           tablefmt="fancy_grid", maxcolwidths=25))
            print()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()


def view_by_user(database, username):
    """Queries database for tickets associated with a specific username"""
    query = "SELECT * FROM tickets WHERE updated_by LIKE ? OR created_by LIKE ? ORDER BY id"
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        cursor.execute(query, (username, username))
        tickets = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
    if tickets:
        print(tabulate(tickets, headers=["ID", "Sev", "Title", "Status", "Info", "Updated by",
                                         "Created by", "Date Updated", "Date Created"],
                       tablefmt="fancy_grid", maxcolwidths=25))
        print()
        return True
    return False


def view_by_severity(database, severity):
    """Queries database for severity, prints results"""
    query = "SELECT * FROM tickets WHERE severity LIKE ? ORDER BY id"
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        cursor.execute(query, severity)
        tickets = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
    if tickets:
        print(tabulate(tickets, headers=["ID", "Sev", "Title", "Status", "Info", "Updated by",
                                         "Created by", "Date Updated", "Date Created"],
                       tablefmt="fancy_grid", maxcolwidths=25))
        print()
        return True
    return False


def view_by_title(database, title):
    """Queries database by title, prints results"""
    query = "SELECT * FROM tickets WHERE title LIKE ? ORDER BY title"
    search = f"%{title}%"
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        cursor.execute(query, (search,))
        tickets = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
    if tickets:
        print(tabulate(tickets, headers=["ID", "Sev", "Title", "Status", "Info", "Updated by",
                                         "Created by", "Date Updated", "Date Created"],
                       tablefmt="fancy_grid", maxcolwidths=25))
        print()
        return True
    return False


def find_ticket(database):
    """Prompts user for id, searches for id or offers other options"""
    if prompt_for_id() == "n":
        choice = ticket_view_options()
        if not choose_ticket_view(database, choice):
            return False
        return find_ticket(database)
    print()
    return find_ticket_by_id(database)


def return_ticket(database, ticket_id):
    """queries database by id and returns ticket as a list"""
    try:
        db_connection = sqlite3.connect(database)
        cursor = db_connection.cursor()
        query = "SELECT * FROM tickets WHERE id = ?;"
        cursor.execute(query, (str(ticket_id),))
        ticket = cursor.fetchone()
        cursor.close()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
    if ticket:
        return ticket
    return False


def update_db_ticket(database, ticket):
    """Updates a ticket in the database"""
    query = """
    UPDATE tickets 
    SET severity = ?, 
    title = ?, 
    status = ?,
    info = ?, 
    updated_by = ?,
    date_updated = ? 
    WHERE 
    id = ?
    """
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        datetime_updated = str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(query, (ticket.sev, ticket.title, ticket.status,
                       ticket.info, ticket.updated_by, datetime_updated, ticket.id))
        db_connection.commit()  # persists changes to the db
        cursor.close()  # closes db cursor object
        print("Ticket updated successfully")
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()


def delete_ticket(database):
    """Finds a ticket id, prompts user and then calls a function to delete the ticket by id"""
    ticket = find_ticket(database)
    if not ticket:
        return False

    choice = ""
    while choice not in ("y","n"):
        choice = input(
            f"""Are you sure you would like to delete the above 
            ticket (ID:'{ticket[0]}')? (y/n): """).strip().lower()
        print()
    if choice == "y":
        delete_ticket_by_id(database, ticket[0])
        return True
    print("The ticket has not been deleted")
    return False


def delete_ticket_by_id(database, ticket_id):
    """deletes a ticket from the database, by id"""
    query = "DELETE FROM tickets WHERE id = ?"
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        cursor.execute(query, (ticket_id,))
        db_connection.commit()  # persists changes to the db
        print("Ticket successfully deleted from database")
        cursor.close()  # closes db cursor object
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
