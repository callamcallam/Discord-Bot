import nextcord, os, datetime, asyncio
from nextcord.ext import commands
from utils.sqlitedatabase import Database
from typing import Optional

class NoteBrowser:
    """A class to browse through notes interactively."""
    def __init__(self, bot, interaction, notes):
        self.bot = bot
        self.interaction = interaction
        self.notes = notes
        self.current_note_index = 0
        self.message = None

    def embed_note(self, note):
        """Create an embed for a specific note."""
        discord_id, steam_hex, fivem, note_text, noted_by, note_date, noted_user, unique_key = note
        embed = nextcord.Embed(
            title=f"Note {self.current_note_index + 1}/{len(self.notes)}",
            description="Details of the note.",
            color=nextcord.Color.red()
        )

        # Add fields to the embed for each piece of note information
        embed.add_field(name="Noted User", value=noted_user or "N/A", inline=False)
        embed.add_field(name="Discord ID", value=f"<@{discord_id}>" if discord_id else "N/A", inline=False)
        embed.add_field(name="Steam Hex", value=steam_hex or "N/A", inline=False)
        embed.add_field(name="FiveM Identifer", value=fivem or "N/A", inline=False)
        embed.add_field(name="Note", value=note_text or "N/A", inline=False)
        embed.add_field(name="Noted By", value=noted_by, inline=False)
        embed.add_field(name="Note Date", value=note_date, inline=False)
        embed.set_footer(text=f"Unique Key: {unique_key}")

        return embed

    async def start(self):
        """Start the note browsing session."""
        self.message = await self.interaction.followup.send(embed=self.embed_note(self.notes[self.current_note_index]))
        
        # Add "previous" and "next" reactions
        await self.message.add_reaction("⬅️")
        await self.message.add_reaction("➡️")

        def check(reaction, user):
            """Check if the reaction is valid."""
            return user == self.interaction.user and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == self.message.id

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                if str(reaction.emoji) == "➡️" and self.current_note_index < len(self.notes) - 1:
                    self.current_note_index += 1
                    await self.message.edit(embed=self.embed_note(self.notes[self.current_note_index]))
                    await self.message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⬅️" and self.current_note_index > 0:
                    self.current_note_index -= 1
                    await self.message.edit(embed=self.embed_note(self.notes[self.current_note_index]))
                    await self.message.remove_reaction(reaction, user)

            except nextcord.errors.Forbidden:
                pass  # Ignore if bot doesn't have reaction management permissions
            except asyncio.TimeoutError:
                break  # End the loop if no reaction is added within the timeout

        # Remove reactions when done
        try:
            await self.message.clear_reactions()
        except nextcord.errors.Forbidden:
            pass

class findNote(commands.Cog):
    """A cog to find and display notes."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(
        name='notes',
        description='Find a note using any identifier',
        force_global=True
    )
    async def _find(
        self, 
        interaction: nextcord.Interaction, 
        identifier: str = nextcord.SlashOption(name="identifier", description="Enter an identifier (Discord ID, Steam Hex, or FiveM ID).", required=True),
    ):
        """Find a note using an identifier."""
        if nextcord.utils.get(interaction.guild.roles, id=self.db.staffRole()) in interaction.user.roles:
            await interaction.response.defer()

            database = Database()
            noted_users, total_note_count = database.findNote(identifier)

            if noted_users:
                browser = NoteBrowser(self.bot, interaction, noted_users)
                await browser.start()
            else:
                await interaction.followup.send("No notes found.")
        else:
            await interaction.response.send_message("You are not staff.", ephemeral=True)

def setup(bot: commands.Bot):
    """Set up the cog."""
    bot.add_cog(findNote(bot))
