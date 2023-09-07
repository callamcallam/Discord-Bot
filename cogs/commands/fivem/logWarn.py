import nextcord
from nextcord.ext import commands
from utils.sqlitedatabase import Database 
from typing import Optional
from datetime import datetime

class logWarn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(
        name='log-warn',
        description='Log a warning into the database.',
        force_global=True
    )
    async def _logwarn(
        self, 
        interaction: nextcord.Interaction, 
        warned_username: Optional[str] = nextcord.SlashOption(name="warned_username", description="Enter the username of the player being banned. This is required!.", required=True),
        discord_id: str = nextcord.SlashOption(name="discord_id", description="Enter the user's Discord ID.", required=False),
        steam_hex: str = nextcord.SlashOption(name="steam_hex_identifer", description="Enter the user's Steam hex.", required=False),
        fivem: str = nextcord.SlashOption(name="fivem_identifer", description="Enter the user's FiveM ID.", required=False),
        evidence: str = nextcord.SlashOption(name="evidence", description="Enter the evidence for the warning.", required=False),
        reason: str = nextcord.SlashOption(name="reason", description="Enter the reason for the warning.", required=False)
    ):
        """
        Logs a warning into the database.
        
        Parameters:
        - warned_username: The username of the player being warned (required).
        - discord_id: The user's Discord ID (optional).
        - steam_hex: The user's Steam hex identifier (optional).
        - fivem: The user's FiveM ID (optional).
        - evidence: The evidence for the warning (optional).
        - reason: The reason for the warning (optional).
        """
        if nextcord.utils.get(interaction.guild.roles, id=self.db.staffRole()) in interaction.user.roles:
            await interaction.response.defer()

            database = Database()

            time = datetime.now()
            warn_date = time.strftime("%B %d, %Y, %I:%M:%S %p")


            database.addWarn(discord_id=discord_id, steam_hex=steam_hex, fivem=fivem, evidence=evidence, reason=reason, warn_date=warn_date, warned_by=interaction.user.display_name, warned_user=warned_username)

            logged = nextcord.Embed(
                title="Warn Recorded",
                description="You have successfully logged a warn.",
                color=nextcord.Color.green(),
                timestamp=datetime.now()

            )
            if warned_username:
                logged.add_field(name="Warned User", value=warned_username, inline=False)
            else:
                logged.add_field(name="Warned User", value="N/A", inline=False)
            if discord_id:
                logged.add_field(name="Discord ID", value=f"<@{discord_id}>", inline=False)
            else:
                logged.add_field(name="Discord ID", value="N/A", inline=False)
            if steam_hex:
                logged.add_field(name="Steam Hex", value=steam_hex, inline=False)
            else:
                logged.add_field(name="Steam Hex", value="N/A", inline=False)
            if fivem:
                logged.add_field(name="FiveM Identifier", value=fivem, inline=False)
            else:
                logged.add_field(name="FiveM Identifier", value="N/A", inline=False)
            if reason:
                logged.add_field(name="Reason", value=reason, inline=False)
            else:
                logged.add_field(name="Reason", value="N/A", inline=False)
            if evidence:   
                logged.add_field(name="Evidence", value=evidence, inline=False)
            else:
                logged.add_field(name="Evidence", value="N/A", inline=False)
            logged.add_field(name="Recorded By", value=interaction.user.display_name, inline=False)
            await interaction.followup.send(embed=logged)
        else:
                await interaction.response.send_message("You are not staff.", ephemeral=True)
                
def setup(bot: commands.Bot):
    bot.add_cog(logWarn(bot))
