"""Module defines functions that interface the sqlite3 database"""

import sqlite3
import datetime
import logging
from tabulate import tabulate


logger = logging.getLogger(__name__)


# TEST DB
def db_test(database):
    """Inits db, logs connection and sqlite3 version. If table doesn't exist, new one is created.
    Returns True if no errors, otherwise returns False and logs errors"""

    table_query = f"""
    CREATE TABLE IF NOT EXISTS {database["table_name"]}(
            id INTEGER PRIMARY KEY,
            severity INTEGER,
            title TEXT,
            status TEXT,
            info TEXT,
            updated_by TEXT,
            created_by TEXT,
            date_updated TEXT,
            date_created TEXT)
    """

    try:
        # opens or creates a sqlite3 db and inits a cursor
        db_connection = sqlite3.connect(database["db_name"])
        cursor = db_connection.cursor()
        logger.info("connected to db: %s", database["db_name"])

        # Gets version no. of sqlite3 for logger
        cursor.execute("SELECT sqlite_version();")
        db_version = cursor.fetchall()
        logger.info("SQLite Database version: %s", db_version[0][0])

        # Checks for valid table in db
        if not db_table_test(database, cursor):
            print(
                """IMPORTANT:

Database doesn't contain a valid table, see logs for more info.
New table has now been created.
System is ready to use.
"""
            )
            cursor.execute(table_query)
            db_connection.commit()

        cursor.close()
        return True

    except sqlite3.Error as error:
        logger.exception(error)
        return False

    finally:
        if db_connection:
            db_connection.close()
            logger.info("db connection closed")


# TEST TABLE
def db_table_test(database, cursor):
    """Tests the db file to assert whether a table exists, if not a new table is created"""

    try:
        cursor.execute(
            """SELECT name 
            FROM sqlite_master 
            WHERE type='table' 
            AND name = ?""",
            (database["table_name"],),
        )

        test_result = cursor.fetchone()

        if not test_result:
            logger.error("no valid table found in database")
            return False

        logger.info("valid table (%s) found in database", database["table_name"])
        return True

    except sqlite3.Error as error:
        logger.exception(error)
        return False


# COUNT
def count_tickets(database):
    """Function counts tickets in db and returns an int"""
    try:
        db_connection = sqlite3.connect(database["db_name"])
        logger.info("connected to db")
        cursor = db_connection.cursor()

        db_init_query = "SELECT COUNT(*) FROM tickets;"
        cursor.execute(db_init_query)
        tickets_amount = cursor.fetchone()[0]
        cursor.close()
        logger.info("There are %s tickets in the db", tickets_amount)
        print(
            f"*** There are currently {tickets_amount} tickets stored in the STS database ***\n"
        )
        return tickets_amount

    except sqlite3.Error as error:
        logger.exception(error)
        return False

    finally:
        if db_connection:
            db_connection.close()
            logger.info("db connection closed")


# CREATE
def insert_ticket_to_db(database, ticket):
    """Function inserts a new ticket into the database"""

    query = """INSERT INTO tickets (severity,title,status,info,updated_by,created_by,
    date_updated,date_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

    try:
        db_connection = sqlite3.connect(database["db_name"])
        logger.info("connected to db")
        cursor = db_connection.cursor()

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
        db_connection.commit()
        logger.info("ticket successfully inserted into db")
        cursor.close()
        print("Ticket successfully saved into database\n")
        return True

    except sqlite3.Error as error:
        logger.exception(error)
        return False

    finally:
        if db_connection:
            db_connection.close()
            logger.info("db connection closed")


# READ
def search_database(database, category, search, order="id"):
    """Function dynamically searches database based on user input,
    prints to screen and returns result"""

    if category == "username":
        query = f"SELECT * FROM tickets WHERE created_by OR updated_by LIKE ? ORDER BY {order}"
    else:
        query = f"SELECT * FROM tickets WHERE {category} LIKE ? ORDER BY {order}"

    try:
        table = False
        db_connection = sqlite3.connect(database["db_name"])
        logger.info("connected to db")
        cursor = db_connection.cursor()
        cursor.execute(query, (str(search),))
        table = cursor.fetchall()
        logger.info("db successfully searched")
        cursor.close()

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
            logger.info("ticket/s found & displayed to user")
        return table

    except sqlite3.Error as error:
        logger.exception(error)
        return False

    finally:
        if db_connection:
            db_connection.close()
            logger.info("db connection closed")


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
        db_connection = sqlite3.connect(database["db_name"])
        logger.info("connected to db")
        cursor = db_connection.cursor()
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
        db_connection.commit()
        logger.info("ticket id:%s successfully updated in db", str(ticket.i_d))
        cursor.close()
        print("Ticket updated successfully\n")
        return True

    except sqlite3.Error as error:
        logger.exception(error)
        return False

    finally:
        if db_connection:
            db_connection.close()
            logger.info("db connection closed")


# DELETE
def delete_ticket_by_id(database, ticket_id):
    """deletes a ticket from the database, by id"""

    query = "DELETE FROM tickets WHERE id = ?"

    try:
        db_connection = sqlite3.connect(database["db_name"])
        logger.info("connected to db")
        cursor = db_connection.cursor()
        cursor.execute(query, (ticket_id,))
        db_connection.commit()
        logger.info("ticket id:%s deleted from db", ticket_id)
        print(f"Ticket id: {ticket_id} permanently deleted from database\n")
        cursor.close()
        return True

    except sqlite3.Error as error:
        logger.exception(error)
        return False

    finally:
        if db_connection:
            db_connection.close()


def find_id_range(database):
    """Queries database for min and max ids, returns a list of two ints"""

    query = "SELECT MIN(id), MAX(id) FROM tickets"

    try:
        db_connection = sqlite3.connect(database["db_name"])
        logger.info("connected to db")
        cursor = db_connection.cursor()
        cursor.execute(query)
        min_max_ids = cursor.fetchall()
        logger.info("db id range found")
        cursor.close()
        return min_max_ids

    except sqlite3.Error as error:
        logger.exception(error)
        return False

    finally:
        if db_connection:
            db_connection.close()
            logger.info("db connection closed")


def view_all_tickets(database):
    """Function displays all tickets in database"""

    query = "SELECT * FROM tickets;"

    try:
        db_connection = sqlite3.connect(database["db_name"])
        cursor = db_connection.cursor()
        logger.info("connected to db")
        cursor.execute(query)
        table = cursor.fetchall()
        logger.info("db successfully searched")
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
            logger.info("all tickets found & displayed to user")
        return True

    except sqlite3.Error as error:
        logger.exception(error)
        return False

    finally:
        if db_connection:
            db_connection.close()
            logger.info("db connection closed")
