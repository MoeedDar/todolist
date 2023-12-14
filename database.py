import sqlite3

class Database:
    def __init__(self, path):
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._cursor = self._conn.cursor()

    def execute(self, query, parameters=()):
        self._cursor.execute(query, parameters)
        self._conn.commit()

    def execute_fetchall(self, query, parameters=()):
        self.execute(query)
        return self._cursor.fetchall()
