import nextcord
from nextcord.ext import commands
from utils.sqlitedatabase import Database

db = Database()
bot = commands.Bot(command_prefix=db.execute("SELECT prefix FROM `Config`;", fetch=True)[0][0], intents=nextcord.Intents.all(), case_insensitive=False, help_command=None)


bot.run(db.execute("SELECT token FROM `Config`;", fetch=True)[0][0])
