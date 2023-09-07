import nextcord
from nextcord.ext import commands
from utils.sqlitedatabase import Database

class UnbanUser(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()
    @nextcord.slash_command(name="unban-user", description="Unban a user",force_global=True)
    @commands.has_permissions(ban_members=True)
    async def unban_user(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str = None):
        if reason == None:
            reason = "No reason provided."
        if self.db.execute("SELECT * FROM `Discord Bans` WHERE `user-id` = ?;", (member.id,), fetch=True):
            self.db.execute("DELETE FROM `Discord Bans` WHERE `user-id` = ?;", (member.id,), commit=True)
            await interaction.guild.unban(user=member, reason=reason)
            await interaction.response.send_message(content=f"{member.mention} has been unbanned! Reason: {reason}", ephemeral=False)
        else:
            await interaction.response.send_message(content=f"{member.mention} is not banned!", ephemeral=False)

def setup(bot:commands.Bot):
    bot.add_cog(UnbanUser(bot))
