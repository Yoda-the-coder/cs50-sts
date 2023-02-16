"""Module defines 'Ticket' class to be used by STS"""

import sts_db_ops
import sts_ticket_ops


class Ticket:
    """Creates a 'ticket' object, populating all relevant data fields."""

    def __init__(self, severity, title, info, username):
        # constructor
        self.i_d = 0
        self.sev = int(severity)
        self.title = str(title)
        self.statuses = {
            1: "created",
            2: "awaiting response",
            3: "in process",
            4: "closed"}
        self.status = self.statuses[1]
        self.info = str(info)
        self.username = str(username)

    def __str__(self):
        return f"""
        Ticket ID: {self.i_d}
        Ticket Sev: {self.sev}
        Ticket Title: {self.title}
        Ticket Status: {self.status}
        Ticket Info: {self.info}
        Employee ID: {self.username}
        """

    def print_ticket(self):
        """Method to print the ticket.
        """
        print(self)

    def save_ticket(self, database, command):
        """Method saves ticket into the db - TO BE MOVED
        """
        choice = ""
        while choice.lower() != "y" and choice.lower() != "n":
            choice = input("Would you like to save the ticket? (y/n): ")
            print()
        if choice.lower() == "n":
            choice_valid = ""
            while choice_valid.lower() != "y" and choice_valid.lower() != "n":
                choice_valid = input(
                    "Are you sure you would like to delete the ticket? (y/n): ")
                print()
            if choice_valid.lower() == "y":
                return
        if command == "create":
            sts_db_ops.insert_ticket_to_db(database, self)

        if command == "update":
            sts_db_ops.update_db_ticket(database, self)

    def update_ticket(self):
        """Method updates the ticket - NEEDS REFACTORING
        """
        choice = 0
        user = sts_ticket_ops.get_user()

        print("""

        1: Severity
        2: Title
        3: Status
        4: Info

        """)

        while choice > 4 or choice < 1:
            try:
                choice = int(input("Select a field to update: "))
                print()
            except ValueError:
                print("User must input a number (1 - 4)")

        match choice:
            case 1:
                self.sev = sts_ticket_ops.get_ticket_sev()
                self.username = user
            case 2:
                self.title = sts_ticket_ops.get_ticket_title()
                self.username = user
            case 3:
                self.status = sts_ticket_ops.get_ticket_status()
                self.username = user
            case 4:
                self.info = sts_ticket_ops.get_ticket_info("y")
                self.username = user
