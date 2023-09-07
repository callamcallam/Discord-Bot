import nextcord
from nextcord.ext import commands
from utils.sqlitedatabase import Database 

class removeNote(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(
        name='remove-note',
        description='Delete a note about a user.',
        force_global=True
    )
    async def _delnote(
        self, 
        interaction: nextcord.Interaction, 
        note_id: str = nextcord.SlashOption(name="unique_key", description="Enter the unique ID for the note.", required=True),
    ):
        """
        Deletes a note about a user.
        
        Parameters:
        - note_id: The unique ID of the note to be deleted (required).
        """
        if nextcord.utils.get(interaction.guild.roles, id=self.db.staffRole()) in interaction.user.roles:
            deleted, e = self.db.delNote(note_id=note_id)
            if deleted:
                await interaction.response.send_message("Deleted note!")
            else:
                await interaction.response.send_message(f"Failed to delete note: {note_id}. Error: {e}")

        else:
                await interaction.response.send_message("You are not staff.", ephemeral=True)
                
def setup(bot: commands.Bot):
    bot.add_cog(removeNote(bot))
