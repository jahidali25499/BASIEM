# Script to access SQL Database- Can be imported to other modules for convenience


import mysql.connector
from config import Config



class SQL_Database:

    def __init__(self):

        credentials = Config()

        self.mydb = mysql.connector.connect(
                host = credentials.host,
                user = credentials.user,
                passwd = credentials.passwd,
                database = credentials.database
                )

        '''
        To use:
        create Object e.g. sql = SQL_Database()
        Create Cursor e.g. cursor = sql.mydb.cursor()

        '''

