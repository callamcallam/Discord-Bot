import nextcord, os
from nextcord.ext import commands
from utils.sqlitedatabase import Database

db = Database()
bot = commands.Bot(command_prefix=db.execute("SELECT prefix FROM `Config`;", fetch=True)[0][0], intents=nextcord.Intents.all(), case_insensitive=False, help_command=None)

for dir in os.listdir("cogs/"):
    cogs = ["leave", "moderation", "tickets", "welcome"]
    if dir.lower() in cogs:
        for command in os.listdir(f"cogs/{dir}/"):
            if command.endswith(".py"):
                bot.load_extension(f"cogs.{dir}.{command[:-3]}")
    else:
        print('Invalid cog directory. Please check the "cogs" folder for any errors.')


bot.run(db.execute("SELECT token FROM `Config`;", fetch=True)[0][0])
