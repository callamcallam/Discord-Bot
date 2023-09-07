import nextcord
import datetime
from nextcord.ext import commands
from utils.sqlitedatabase import Database 
from typing import Optional

class logNote(commands.Cog):
    """A cog to log notes."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(
        name='log-note',
        description='Add a note to a player',
        force_global=True
    )
    async def _lognote(
        self, 
        interaction: nextcord.Interaction, 
        noted_user: Optional[str] = nextcord.SlashOption(name="note_username", description="Enter the username of the player for their notes. This is required!.", required=True),
        note: Optional[str] = nextcord.SlashOption(name="note", description="Enter the note of the player for their notes. This is required!.", required=True),
        discord_id: Optional[str] = nextcord.SlashOption(name="discord_id", description="Enter the user's Discord ID if known. Otherwise, leave blank.", required=False),
        steam_hex: Optional[str] = nextcord.SlashOption(name="steam_hex_identifer", description="Enter the user's Steam hex", required=False),
        fivem: Optional[str] = nextcord.SlashOption(name="fivem_identifer", description="Enter the user's FiveM ID", required=False),
    ):
        """Log a note for a player."""
        if nextcord.utils.get(interaction.guild.roles, id=self.db.staffRole()) in interaction.user.roles:

            logged = nextcord.Embed(
                title="Note Recorded",
                description="You have successfully logged a note.",
                color=nextcord.Color.green(),
                timestamp=datetime.datetime.now()
            )

            # Add fields to the embed for each piece of note information
            logged.add_field(name="User", value=noted_user or "N/A", inline=False)
            logged.add_field(name="Discord ID", value=f"<@{discord_id}>" if discord_id else "N/A", inline=False)
            logged.add_field(name="Steam Hex", value=steam_hex or "N/A", inline=False)
            logged.add_field(name="FiveM Identifer", value=fivem or "N/A", inline=False)
            logged.add_field(name="Note", value=note, inline=False)
            logged.add_field(name="Recored By", value=interaction.user.display_name, inline=False)

            time = datetime.datetime.now()
            readable_time = time.strftime("%B %d, %Y, %I:%M:%S %p")

            database = Database()
            result = database.addNote(note_name=noted_user, discord_id=discord_id, steam_hex=steam_hex, fivem=fivem, note_by=interaction.user.display_name, note_date=str(readable_time), note=note)

            # Check if the note was logged successfully
            if isinstance(result, tuple):
                success, error = result
            else:
                success = result
                error = None

            if success:
                await interaction.response.send_message(embed=logged)
            else:
                await interaction.response.send_message(f"Error inserting note into database. Error code: {str(error)}")
        else:
            await interaction.response.send_message("You are not staff.", ephemeral=True)

def setup(bot: commands.Bot):
    """Set up the cog."""
    bot.add_cog(logNote(bot))
