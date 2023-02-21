"""Module defines 'Ticket' class to be used by STS"""


class Ticket:
    """Creates a 'ticket' object, populating all relevant data fields."""

    def __init__(self, severity, title, info, username):
        # constructor
        self.i_d = 0
        self.sev = int(severity)
        self.title = str(title)
        self.statuses = {
            1: "Created",
            2: "Awaiting Response",
            3: "In Process",
            4: "Closed",
        }
        self.status = self.statuses[1]
        self.info = str(info)
        self.username = str(username)

    def __str__(self):
        return f"""
        Ticket Sev: {self.sev}
        Ticket Title: {self.title}
        Ticket Status: {self.status}
        Ticket Info: {self.info}
        Employee ID: {self.username}
        """

    def print_ticket(self):
        """Method to print the ticket."""
        print(self)
