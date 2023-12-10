# simple-ticketing-system

### Video Demo: https://youtu.be/TcuxjaBDfq4

### Short Description
A python CLI application for CRUD tickets, using SQLite

### Dependencies:
Tabulate

### Installation
To install dependencies either:
'pip install -r requirements.txt'

or:
'pip install tabulate'

### Instructions
To run Simple Ticketing System, 'cd' into 'simple-ticketing-system' dir and enter 'python3 main.py'.
All log files are stored in ./logs.
Database is stored in ./database

# Info
On first execution the app will detect whether a valid database exists and create a new one if it doesn't. The CLI will prompt will notify the user of this and logs can be found in the 'logs' directory.

The main.py file is the main scripty that is executed, a logger is created and the the functions for each CLI option all live within this file. The 'sts_db_ops.py' script contains all of the CRUD logic for interfacing with the database. SQLite3 is utilised as a database engine for this application. 'sts_logging.py' is a simple decorator function that is utilised throughout the code to log specific function calls. 

A class - 'Ticket' lives within the 'sts_ticket.py' file, this is the class that all ticket objects will be created from within the application. The sts_user_inputs.py' file contains a number of helper functions that are utilised for al of the user input within the app. This is for sanitizing input and also providing reusability.

The application, once running, provides users the availability to create new tickets with an ID (created by the app), title, severity, status and their username will be attached on creation. The user will be prompted throughout to validate input and finally prompted whether to persist the ticket into the database or delete it, if the user opts to save the ticket it will be stored within the SQLite3 'sts_database.db'. 

Tickets can be viewed via several different methods. All tickets can be viewed or searches can be run on the database, finding tickets through id, username, severity, title or description. All of these tickets are displayed in a table format in the CLI utilising the 'tabulate' library. 

Tickets can also be updated and the update functionality provides the user a way to find the ticket they are looking to update before then updating it and finally saving the update to the database. The user that updates the ticket wil have their username attached to the ticket. Finally, tickets can also be deleted from the databse, in a similar way to the update method, the ticket will be found via a sarch and the user can then confirm whether or not to delete the ticket.