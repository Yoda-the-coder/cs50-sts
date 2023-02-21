"""Module defines functions that interface the sqlite3 database"""

import sqlite3
import datetime
from tabulate import tabulate


def db_error(error):
    """Function prints database error code when sqlite3 error raised"""
    print(f"Database Error: {error} ")
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
            f"*** There are currently {tickets_amount[0]} tickets stored in the STS database ***"
        )
    except sqlite3.Error as error:
        db_error(error)
        raise sqlite3.Error("Error Reading Database")

    if db_connection:
        db_connection.close()
    return tickets_amount[0]


# CREATE
def insert_ticket_to_db(database, ticket):
    """Function inserts a new ticket into the database"""
    query = """INSERT INTO tickets (severity,title,status,info,updated_by,created_by,
    date_updated,date_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        datetime_created = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(
            query,
            (
                ticket.sev,
                ticket.title,
                ticket.status,
                ticket.info,
                ticket.username,
                ticket.username,
                datetime_created,
                datetime_created,
            ),
        )
        db_connection.commit()  # persists changes to the db
        cursor.close()  # closes db cursor object
        print("Ticket successfully saved into database")
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()


# READ
def search_database(database, category, search, order="id"):
    """Function dynamically searches database based on user input,
    prints to screen and returns results"""
    if category == "username":
        query = f"SELECT * FROM tickets WHERE created_by OR updated_by LIKE ? ORDER BY {order}"
    else:
        query = f"SELECT * FROM tickets WHERE {category} LIKE ? ORDER BY {order}"
    try:
        table = False
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        cursor.execute(query, (str(search),))
        table = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
    if table:
        print(
            tabulate(
                table,
                headers=[
                    "ID",
                    "Severity",
                    "Title",
                    "Status",
                    "Info",
                    "Updated by",
                    "Created by",
                    "Date Updated",
                    "Date Created",
                ],
                tablefmt="fancy_grid",
                maxcolwidths=25,
            )
        )
        print()
        return table
    return False


# UPDATE
def update_ticket_to_db(database, ticket):
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
        datetime_updated = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(
            query,
            (
                ticket.sev,
                ticket.title,
                ticket.status,
                ticket.info,
                ticket.username,
                datetime_updated,
                str(ticket.i_d),
            ),
        )
        db_connection.commit()  # persists changes to the db
        cursor.close()  # closes db cursor object
        print("Ticket updated successfully")
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()


# DELETE
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


def find_id_range(database):
    """Queries database for min and max ids, returns a list of two ints"""
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

    if min_max_ids:
        return min_max_ids

    return False


def view_all_tickets(database):
    """Function displays all tickets in database"""
    query = "SELECT * FROM tickets;"
    try:
        db_connection = sqlite3.connect(database)  # connects to db
        cursor = db_connection.cursor()  # creates cursor object
        cursor.execute(query)
        table = cursor.fetchall()
        cursor.close()
        if table:
            print(
                tabulate(
                    table,
                    headers=[
                        "ID",
                        "Sev",
                        "Title",
                        "Status",
                        "Info",
                        "Updated by",
                        "Created by",
                        "Date Updated",
                        "Date Created",
                    ],
                    tablefmt="fancy_grid",
                    maxcolwidths=25,
                )
            )
            print()
    except sqlite3.Error as error:
        db_error(error)
    finally:
        if db_connection:
            db_connection.close()
