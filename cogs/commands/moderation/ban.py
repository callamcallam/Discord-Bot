import nextcord, datetime
from nextcord.ext import commands
from utils.sqlitedatabase import Database
from nextcord.ext import application_checks

class BanUser(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(name="ban-user", description="Ban a user",force_global=True)
    @application_checks.has_permissions(ban_members=True)
    async def ban_user(self, interaction: nextcord.Interaction, user: nextcord.Member, reason: str = None, delete_messages:str = nextcord.SlashOption(name="delete-messages", description="Delete Messages", choices=["Don't Delete Any", "Previous Hour", "Previous 6 Hours", "Previous 12 Hours", "Previous 24 Hours", "Previous 3 Days", "Previous Week"], default="Don't Delete Any")):
        #await interaction.response.defer(ephemeral=True)
        if reason == None:
            reason = "No reason provided."
        if delete_messages == "Previous Hour":
            delete_message_seconds=3600
        elif delete_messages == "Previous 6 Hours":
            delete_message_seconds=21600
        elif delete_messages == "Previous 12 Hours":
            delete_message_seconds=43200
        elif delete_messages == "Previous 24 Hours":
            delete_message_seconds=86400
        elif delete_messages == "Previous 3 Days":
            delete_message_seconds=259200
        elif delete_messages == "Previous Week":
            delete_message_seconds=604800
        else:
            delete_message_seconds=None
        await user.ban(reason=reason, delete_message_seconds=delete_message_seconds)
        self.db.execute(f"INSERT INTO `Discord Bans` (`user-id`, `reason`, `date`, `banned-by`) VALUES ('{user.id}', '{reason}', '{datetime.datetime.now()}','{interaction.user.id}');", commit=True)
        await interaction.response.send_message(content=f"{user.mention} has been banned! Reason: {reason}", ephemeral=False)
        return



def setup(bot:commands.Bot):
    bot.add_cog(BanUser(bot))