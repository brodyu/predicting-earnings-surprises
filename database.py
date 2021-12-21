# Local modules
import os
import math
import datetime

# Third party modules
import sqlite3

DATABASENAME = './earnings_surprise.db'

def run():
    """ Creates and populates the database """
    if os.path.exists(DATABASENAME):
        os.remove(DATABASENAME)
    connection = sqlite3.connect(DATABASENAME)
    create_database(connection)
    populate_database(connection)

def create_database(connection):
    pass

def populate_database(connection):
    pass