import psycopg2
from src.config.Config import PGHOST, PGDATABASE, PGUSER, PGPASSWORD

class SingletonException(Exception):
    pass

class DBConnection:
    __instance = None

    @staticmethod
    def get_instance():
        if DBConnection.__instance is None:
            DBConnection()
        return DBConnection.__instance

    def __init__(self):
        if DBConnection.__instance is not None:
            raise SingletonException("Esta clase es un singleton, no se puede crear más de una instancia.")
        else:
            self.connection = psycopg2.connect(
                host=PGHOST,
                database=PGDATABASE,
                user=PGUSER,
                password=PGPASSWORD,
                sslmode='require'
            )
            self.cursor = self.connection.cursor()
            DBConnection.__instance = self