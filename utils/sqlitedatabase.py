import sqlite3
import asyncio

class Database:
    def __init__(self):
        self.db = sqlite3.connect('CCRP Bot.db')
        self.cursor = self.db.cursor()

    def execute(self, sql, values: tuple = None, fetch: bool = False, commit: bool = False):
        if values:
            self.cursor.execute(sql, values)
        else:
            self.cursor.execute(sql)
        if commit:
            self.db.commit()
        if fetch:
            return self.cursor.fetchall()