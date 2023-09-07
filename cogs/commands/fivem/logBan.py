import nextcord
import datetime
from nextcord.ext import commands
from utils.sqlitedatabase import Database 
from typing import Optional

class logBan(commands.Cog):
    """A cog to log bans."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(
        name='log-ban',
        description='Log a ban given in game.',
        force_global=True
    )
    async def _logban(
        self, 
        interaction: nextcord.Interaction, 
        banned_user: Optional[str] = nextcord.SlashOption(name="banned_username", description="Enter the username of the player being banned. This is required!.", required=True),
        discord_id: Optional[str] = nextcord.SlashOption(name="discord_id", description="Enter the user's Discord ID if known. Otherwise, leave blank.", required=False),
        steam_hex: Optional[str] = nextcord.SlashOption(name="steam_hex_identifer", description="Enter the user's Steam hex", required=False),
        fivem: Optional[str] = nextcord.SlashOption(name="fivem_identifer", description="Enter the user's FiveM ID", required=False),
        reason: Optional[str] = nextcord.SlashOption(name="reason_for_ban", description="Enter the reason for the ban", required=False),
        duration: Optional[str] = nextcord.SlashOption(name="ban_duration", description="Enter the duration of the ban", required=False),
        evidence: Optional[str] = nextcord.SlashOption(name="evidence_for_ban", description="Enter the evidence for the ban", required=False)
    ):
        """Log a ban given in game."""
        if nextcord.utils.get(interaction.guild.roles, id=self.db.staffRole()) in interaction.user.roles:

            logged = nextcord.Embed(
                title="Ban Recorded",
                description="You have successfully logged a ban.",
                color=nextcord.Color.green(),
                timestamp=datetime.datetime.now()
            )

            # Add fields to the embed for each piece of ban information
            logged.add_field(name="Banned User", value=banned_user or "N/A", inline=False)
            logged.add_field(name="Discord ID", value=f"<@{discord_id}>" if discord_id else "N/A", inline=False)
            logged.add_field(name="Steam Hex", value=steam_hex or "N/A", inline=False)
            logged.add_field(name="FiveM Identifer", value=fivem or "N/A", inline=False)
            logged.add_field(name="Reason", value=reason or "N/A", inline=False)
            logged.add_field(name="Duration", value=duration or "N/A", inline=False)
            logged.add_field(name="Evidence", value=evidence or "N/A", inline=False)
            logged.add_field(name="Recored By", value=interaction.user.display_name, inline=False)

            time = datetime.datetime.now()
            readable_time = time.strftime("%B %d, %Y, %I:%M:%S %p")

            database = Database()
            result = database.addBan(discord_id=discord_id, steam_hex=steam_hex, fivem=fivem,reason=reason, evidence=evidence, duration=duration, banned_by=interaction.user.display_name,ban_date=str(readable_time), banned_user=banned_user)

            # Check if the ban was logged successfully
            if isinstance(result, tuple):
                success, error = result
            else:
                success = result
                error = None

            if success:
                await interaction.response.send_message(embed=logged)
            else:
                await interaction.response.send_message(f"Error inserting ban into database. Error code: {str(error)}")
        else:
            await interaction.response.send_message("You are not staff.", ephemeral=True)

def setup(bot: commands.Bot):
    """Set up the cog."""
    bot.add_cog(logBan(bot))
