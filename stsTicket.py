import datetime

import stsDBOps
import stsTicketOps


class Ticket:
    def __init__(self, sev, title, info, created_by, date_created):
        # constructor
        self.id = 0
        self.sev = int(sev)
        self.title = str(title)
        self.statuses = {
        1: "created", 
        2: "awaiting response", 
        3: "in process", 
        4: "closed"}
        self.status = self.statuses[1]
        self.info = str(info)
        self.updated_by = str(created_by)
        self.created_by = str(created_by)
        self.date_created = date_created
        self.date_updated = date_created
    

    def __str__(self):
        return f"""
        Ticket ID: {self.id}
        Ticket Sev: {self.sev}
        Ticket Title: {self.title}
        Ticket Status: {self.status}
        Ticket Info: {self.info}
        Created By: {self.created_by}
        Updated By: {self.updated_by}
        Date Created: {self.date_created}
        Date Updated: {self.date_updated}
        """


    def print_ticket(self):
        print(self)


    def save_ticket(self, database, command):
        choice = ""
        while not choice.lower() == "y" and not choice.lower() == "n":
            choice = input("Would you like to save the ticket? (y/n): ")
            print()
        if choice.lower() == "n":
            choice_valid = ""
            while not choice_valid.lower() == "y" and not choice_valid.lower() == "n":
                choice_valid = input("Are you sure you would like to delete the ticket? (y/n): ")
                print()
            if choice_valid.lower() == "y":
                return
        if command == "create":    
            stsDBOps.insert_ticket_to_db(database, self)

        if command == "update":
            stsDBOps.update_db_ticket(database, self)
            

    def update_ticket(self):
        choice = 0
        user = stsTicketOps.get_user()

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
                self.sev = stsTicketOps.get_ticket_sev()
                self.updated_by = user
                self.date_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")                
            case 2:
                self.title = stsTicketOps.get_ticket_title()
                self.updated_by = user
                self.date_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")                
            case 3:
                self.status = stsTicketOps.get_ticket_status()
                self.updated_by = user
                self.date_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")                
            case 4:
                self.info = stsTicketOps.get_ticket_info("y")
                self.updated_by = user
                self.date_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
                    
                