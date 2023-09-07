import nextcord, os
from nextcord.ext import commands
from utils.sqlitedatabase import Database

db = Database()
bot = commands.Bot(command_prefix=db.execute("SELECT command_prefix FROM `Config`;", fetch=True)[0][0], intents=nextcord.Intents.all(), case_insensitive=False, help_command=None)

# for dir in os.listdir("cogs/commands"):
    #print(dir)
    # try:
    #     cogs = [cog.lower() for cog in os.listdir("cogs/commands")]
    #     if dir.lower() in cogs:
    #         for command in os.listdir(f"cogs/commands/{dir}"):
    #             if command.endswith(".py"):
    #                 #print(command)
    #                 print(f"Loading cogs.{dir}.{command[:-3]}")
    #                 bot.load_extension(f"cogs.{dir}.{command[:-3]}")
    #     else:
    #         print('Invalid cog directory. Please check the "cogs" folder for any errors.')
    # except Exception as e:
    #     print(f"Error loading {dir}: {e}")

for folder in os.listdir("cogs"):
    for subfolder in os.listdir(f"cogs/{folder}"):
        for file in os.listdir(f"cogs/{folder}/{subfolder}"):
            if file.endswith(".py"):
                bot.load_extension(f"cogs.{folder}.{subfolder}.{file[:-3]}")
                print(f"Loaded cogs.{folder}.{subfolder}.{file[:-3]}")


bot.run(db.execute("SELECT token FROM `Config`;", fetch=True)[0][0])
