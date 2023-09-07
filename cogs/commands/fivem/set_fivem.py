import nextcord
from nextcord.ext import commands
from nextcord.ext import application_checks
from utils.sqlitedatabase import Database
class SetFivem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(name="set-fivem", description="Sets the FiveM system up for the server.", force_global=True)
    @application_checks.has_permissions(manage_guild=True)
    async def callback(self, i: nextcord.Interaction, enabled: str = nextcord.SlashOption(name="active", description="Enable/Disable FiveM Logging System!", choices=["Enable", "Disable"], required=True)):
        ...

def setup(bot: commands.Bot):
    bot.add_cog(SetFivem(bot))