import nextcord
from nextcord.ext import commands
from utils.sqlitedatabase import Database

class SetTickets(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.db = Database()


def setup(bot: commands.Bot):
    bot.add_cog(SetTickets(bot))