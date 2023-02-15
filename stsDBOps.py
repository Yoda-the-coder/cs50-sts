import sqlite3

import stsTicketOps
from tabulate import tabulate


def db_error(error):
    print(f"Error connecting to database: {error} ")
    # log error


def db_init(database):
    try:        
        db_connection = sqlite3.connect(database)
        cursor = db_connection.cursor()
        print(f"Successfully connected to STS database: {database}")
        db_init_query = "SELECT sqlite_version();"
        cursor.execute(db_init_query)
        db_version = cursor.fetchall()     
        print(f"SQLite Database version: {db_version[0][0]}")
        cursor.close
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
            print("Database connection test completed successfully")
            print()


def prompt_for_id():
    choice = ""
    while not choice == "y" and not choice == "n":
        choice = input("Do you know the Ticket ID? (y/n): ").strip().lower()
    return choice


def ticket_view_options():
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
    match choice:
        case 1:
            # view all tickets
            print()
            if not view_all_tickets(database):
                print("No tickets found")
                return False
            else:
                return True
                          
        case 2:
            # search by username
            print()
            username = stsTicketOps.get_user()
            print()
            if not view_by_user(database, username):
                print("No tickets found")
                return False
            else:
                return True

        case 3:
            # search by severity
            print()
            severity = stsTicketOps.get_ticket_sev()
            print()
            if not view_by_severity(database, str(severity)):
                print("No tickets found")
                return False
            else:
                return True

        case 4:
            # search by title
            print()
            title = stsTicketOps.get_ticket_title().strip()
            print()
            if not view_by_title(database, title):
                print("No tickets found")
                return False
            else:
                return True

        case 5:
            # return to main menu
            return False


def count_tickets(database):
    try:
        db_connection = sqlite3.connect(database)
        cursor = db_connection.cursor()
        db_init_query = "SELECT COUNT(*) FROM tickets;"
        cursor.execute(db_init_query)
        tickets_amount = cursor.fetchone()
        print(f"There are currently {tickets_amount[0]} tickets stored in the STS database")
        cursor.close
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
        return tickets_amount[0]       


def insert_ticket_to_db(database, ticket):
    query = "INSERT INTO tickets (severity,title,status,info,updated_by,created_by,date_updated,date_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    try:
        db_connection = sqlite3.connect(database) # connects to db
        cursor = db_connection.cursor() # creates cursor object 
        cursor.execute(query, (ticket.sev, ticket.title, ticket.status, ticket.info, ticket.updated_by, ticket.created_by, ticket.date_updated, ticket.date_created))
        db_connection.commit() # persists changes to the db
        print("Ticket successfully saved into database")
        cursor.close() # closes db cursor object
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()


def find_ticket_by_id(database):
    try:
        ticket_id = int(input("Please enter the ticket ID: "))
        print()           
    except ValueError:
        print("Ticket ID must be a number")      
    finally:
        if view_by_id(database, ticket_id):
            return return_ticket(database, ticket_id)
        else:
            print("Ticket ID doesn't exist in database, double check ID")
            print()
            return find_ticket(database)


def view_by_id(database, ticket_id):
    query = "SELECT * FROM tickets WHERE id = ? ORDER BY severity"
    try:
        db_connection = sqlite3.connect(database) # connects to db
        cursor = db_connection.cursor() # creates cursor object
        cursor.execute(query, (ticket_id,))
        ticket = cursor.fetchall()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
    if ticket:
        print(tabulate(ticket, headers=["ID", "Severity", "Title", "Status", "Info", "Updated by", "Created by", "Date Updated", "Date Created"], tablefmt="fancy_grid", maxcolwidths=25))
        print()
        return True
    else:
        return False


def view_all_tickets(database):
    query = "SELECT * FROM tickets;"
    try:
        db_connection = sqlite3.connect(database) # connects to db
        cursor = db_connection.cursor() # creates cursor object 
        cursor.execute(query)
        tickets = cursor.fetchall()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
        if tickets:
            print(tabulate(tickets, headers=["ID", "Sev", "Title", "Status", "Info", "Updated by", "Created by", "Date Updated", "Date Created"], tablefmt="fancy_grid", maxcolwidths=25))
            print()
            return True
        else:
            return False


def view_by_user(database, username):
    query = "SELECT * FROM tickets WHERE updated_by LIKE ? OR created_by LIKE ? ORDER BY id"
    try:
        db_connection = sqlite3.connect(database) # connects to db
        cursor = db_connection.cursor() # creates cursor object
        cursor.execute(query, (username, username))
        tickets = cursor.fetchall()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
        if tickets:
            print(tabulate(tickets, headers=["ID", "Sev", "Title", "Status", "Info", "Updated by", "Created by", "Date Updated", "Date Created"], tablefmt="fancy_grid", maxcolwidths=25))
            print()
            return True
        else:
            return False


def view_by_severity(database, severity):
    query = "SELECT * FROM tickets WHERE severity LIKE ? ORDER BY id"
    try:
        db_connection = sqlite3.connect(database) # connects to db
        cursor = db_connection.cursor() # creates cursor object
        cursor.execute(query, severity)
        tickets = cursor.fetchall()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
        if tickets:
            print(tabulate(tickets, headers=["ID", "Sev", "Title", "Status", "Info", "Updated by", "Created by", "Date Updated", "Date Created"], tablefmt="fancy_grid", maxcolwidths=25))
            print()
            return True
        else:
            return False    


def view_by_title(database, title):
    query = "SELECT * FROM tickets WHERE title LIKE ? ORDER BY title"
    search = f"%{title}%"
    try:
        db_connection = sqlite3.connect(database) # connects to db
        cursor = db_connection.cursor() # creates cursor object
        cursor.execute(query, (search,))
        tickets = cursor.fetchall()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
        if tickets:
            print(tabulate(tickets, headers=["ID", "Sev", "Title", "Status", "Info", "Updated by", "Created by", "Date Updated", "Date Created"], tablefmt="fancy_grid", maxcolwidths=25))
            print()
            return True
        else:
            return False


def find_ticket(database):      
    if prompt_for_id() == "n":
        choice = ticket_view_options()
        if not choose_ticket_view(database, choice):
            return False
        else:
            return find_ticket(database)
    else:
        print()
        return find_ticket_by_id(database)
        

def return_ticket(database, ticket_id):
    try:
        db_connection = sqlite3.connect(database)
        cursor = db_connection.cursor()
        query = "SELECT * FROM tickets WHERE id = ?;"
        cursor.execute(query, (str(ticket_id),))
        ticket = cursor.fetchone()
        cursor.close
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
        return ticket


def update_db_ticket(database, ticket):
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
        db_connection = sqlite3.connect(database) # connects to db
        cursor = db_connection.cursor() # creates cursor object 
        cursor.execute(query, (ticket.sev, ticket.title, ticket.status, ticket.info, ticket.updated_by, ticket.date_updated, ticket.id))
        db_connection.commit() # persists changes to the db
        print("Ticket updated successfully")
        cursor.close() # closes db cursor object
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()


def delete_ticket(database):
    ticket = find_ticket(database)
    if not ticket:
        return False
    else:
        choice = ""
        while not choice == "y" and not choice == "n":
            choice = input(f"Are you sure you would like to delete the above ticket (ID:'{ticket[0]}')? (y/n): ").strip().lower()
            print()
        if choice == "y":
            delete_ticket_by_id(database, ticket[0])
            return True
        else:
            print("The ticket has not been deleted")
            return False


def delete_ticket_by_id(database, ticket_id):
    query = "DELETE FROM tickets WHERE id = ?"
    try:
        db_connection = sqlite3.connect(database) # connects to db
        cursor = db_connection.cursor() # creates cursor object 
        cursor.execute(query, (ticket_id,))
        db_connection.commit() # persists changes to the db
        print("Ticket successfully deleted from database")
        cursor.close() # closes db cursor object
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()