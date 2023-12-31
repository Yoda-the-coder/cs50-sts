"""Module defines 'Ticket' class to be used by STS

File: sts_ticket.py
Disclaimer: The following source code is the sole work of the author unless otherwise stated. 
Copyright (C) Ashley Taylor. All Rights Reserved.
"""

import logging
from sts_logging import log_function

logger = logging.getLogger(__name__)


class Ticket:
    """Creates a 'ticket' object, populating all relevant data fields."""

    @log_function
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
        logger.info("Ticket object created")

    def __str__(self):
        print_format = f"""\t---- Ticket ----
        
        Ticket Sev: {self.sev}
        Ticket Title: {self.title}
        Ticket Status: {self.status}
        Ticket Info: {self.info}
        Employee ID: {self.username}

        ---- End of Ticket ----\n"""
        return print_format

    @log_function
    def print_ticket(self):
        """Method to print the ticket."""
        logger.info("Ticket object printed to screen")
        print(self)
