import nextcord, datetime
from nextcord.ext import commands, application_checks
from utils.sqlitedatabase import Database
class KickUser(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()
    
    @nextcord.slash_command(name='kick-user', description="Kick a user.", force_global=True)
    @application_checks.has_permissions(kick_members=True)
    async def kick_user(self, interaction: nextcord.Interaction, user: nextcord.Member, reason: str = None):
        if reason == None:
            reason = "No reason provided."
        await interaction.guild.kick(user=user, reason=reason)
        self.db.execute(f"INSERT INTO `Discord Kicks` (`user-id`, `reason`, `date`, `kicked-by`) VALUES ('{user.id}', '{reason}', '{datetime.datetime.now()}','{interaction.user.id}');", commit=True)
        await interaction.response.send_message(content=f"{user.mention} has been kicked! Reason: {reason}", ephemeral=False)
        return
    
def setup(bot:commands.Bot):
    bot.add_cog(KickUser(bot))
    