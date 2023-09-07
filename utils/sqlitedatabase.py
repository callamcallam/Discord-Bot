import sqlite3
import asyncio
import random, string

class Database:
    def __init__(self):
        self.db = sqlite3.connect('config/CCRP Bot.db')
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
        
    def addBan(self, discord_id: str, steam_hex, fivem: str,reason: str, evidence: str, duration: str, banned_by: str, ban_date: str, banned_user: str):
        try:
            if discord_id is None:
                discord_id = ""
            elif steam_hex is None:
                steam_hex = "N/A"
            elif fivem is None:
                fivem = "N/A"
            elif evidence is None:
                evidence = "N/A"
            query = "INSERT INTO `FiveM Bans` (`Discord ID`, `Steam Hex`, `FiveM`, `Evidence`, `Reason`, `Banned By`, `Ban Duration`,`Ban Date`, `Banned User`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

            self.db.execute(query, (discord_id, steam_hex, fivem, evidence, reason, banned_by, duration, ban_date, banned_user))
            self.db.commit()
            return True
        except Exception as e:
            return False, e

    def findBan(self, identifier: str):
        columns = ['Banned User', 'Discord ID', 'Steam Hex', 'FiveM']

        ban_records = set()  # To store unique ban records
        matches = []
        for column in columns:
            try:
                search_value = f"%{identifier}%"
                print(f"Executing query: SELECT * FROM `FiveM Bans` WHERE `{str(column)}` LIKE ?")
                self.cursor.execute(f"SELECT * FROM `FiveM Bans` WHERE `{str(column)}` LIKE ?", (search_value,))
                
                match = self.cursor.fetchall()
                if match:
                    print(f"Match found: {match}")
                    matches.extend(match)
                    for row in match:
                        ban_records.add(tuple(row))  # Add the ban record as a tuple
            except Exception as e:
                print(f"Error executing query: {e}")

        total_ban_count = len(ban_records)  # Count of unique `FiveM Bans`
        return matches, total_ban_count

    def addWarn(self, discord_id: str, steam_hex, fivem: str,reason: str, evidence: str, warned_by: str, warn_date: str, warned_user: str):
        try:
            if discord_id is None:
                discord_id = ""
            elif steam_hex is None:
                steam_hex = "N/A"
            elif fivem is None:
                fivem = "N/A"
            elif evidence is None:
                evidence = "N/A"
            query = "INSERT INTO `FiveM Warns` (`Discord ID`, `Steam Hex`, `FiveM`, `Evidence`, `Reason`, `Warned By`,`Warn Date`, `Warned User`) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

            self.db.execute(query, (discord_id, steam_hex, fivem, evidence, reason, warned_by, warn_date, warned_user))
            self.db.commit()
            return True
        except Exception as e:
            return False, e


    def findWarn(self, identifier: str):
        columns = ['Warned User', 'Discord ID', 'Steam Hex', 'FiveM']

        warn_records = set()  # To store unique warn records
        matches = []
        for column in columns:
            try:
                search_value = f"%{identifier}%"
                print(f"Executing query: SELECT * FROM `FiveM Warns` WHERE `{str(column)}` LIKE ?")
                self.cursor.execute(f"SELECT * FROM `FiveM Warns` WHERE `{str(column)}` LIKE ?", (search_value,))
                match = self.cursor.fetchall()
                if match:
                    print(f"Match found: {match}")
                    matches.extend(match)
                    for row in match:
                        warn_records.add(tuple(row))  # Add the warn record as a tuple
            except Exception as e:
                print(f"Error executing query: {e}")

        total_warn_count = len(warn_records)  # Count of unique `FiveM Warns`
        return matches, total_warn_count

    def findNote(self, identifier: str):
        columns = ['Noted User', 'Discord ID', 'Steam Hex', 'FiveM']

        note_records = set()  # To store unique note records
        matches = []
        for column in columns:
            try:
                search_value = f"%{identifier}%"
                print(f"Executing query: SELECT * FROM `FiveM Notes` WHERE `{str(column)}` LIKE ?")
                self.cursor.execute(f"SELECT * FROM `FiveM Notes` WHERE `{str(column)}` LIKE ?", (search_value,))
                match = self.cursor.fetchall()
                if match:
                    print(f"Match found: {match}")
                    matches.extend(match)
                    for row in match:
                        note_records.add(tuple(row))  # Add the note record as a tuple
            except Exception as e:
                print(f"Error executing query: {e}")

        total_note_count = len(note_records)  # Count of unique `FiveM Notes`
        return matches, total_note_count


    def staffRole(self):

        id = self.cursor.execute("SELECT `Staff Team ID` FROM Config;").fetchone()
        id = id[0]
        return id

    def addNote(self, note_name: str,discord_id: str, steam_hex, fivem: str, note: str, note_by: str, note_date):
        try:
            if discord_id is None:
                discord_id = ""
            elif steam_hex is None:
                steam_hex = "N/A"
            elif fivem is None:
                fivem = "N/A"
            query = "INSERT INTO `FiveM Notes` (`Discord ID`, `Steam Hex`, `FiveM`, `Notes`, `Note By`, `Note Date`, `Noted User`, `Unique Key`) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

            self.db.execute(query, (discord_id, steam_hex, fivem, note, note_by, note_date, note_name, Database.randID(self)))
            self.db.commit()
            return True
        except Exception as e:
            return False, e

    def delNote(self, note_id: str):
        try:
            query = f"DELETE FROM `FiveM Notes` WHERE `Unique Key` = '{note_id}';"
            self.cursor.execute(query)
            self.db.commit()
            return True, None
        except Exception as e:
            return False, e
    def randID(self):
        for _ in range(5):
            # Generate a random ID using alphanumeric characters
            id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            return id
    def _del_(self):
        self.db.close()