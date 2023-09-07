import nextcord, asyncio
from nextcord.ext import commands
from utils.sqlitedatabase import Database 
from typing import Optional

class WarnBrowser:
    """A class to browse through warns interactively."""
    def __init__(self, bot, interaction, warns):
        self.db = Database()
        self.bot = bot
        self.interaction = interaction
        self.warns = warns
        self.current_warn_index = 0
        self.message = None

    def embed_warn(self, warn):
        """Create an embed for a specific warn."""
        discord_id, steam_hex, fivem, evidence, reason, warned_by, warn_date, warned_user = warn

        embed = nextcord.Embed(
            title=f"Warn {self.current_warn_index + 1}/{len(self.warns)}",
            description="Details of the warn.",
            color=nextcord.Color.red()
        )

        # Add fields to the embed for each piece of warn information
        embed.add_field(name="Warned User", value=warned_user or "N/A", inline=False)
        embed.add_field(name="Discord ID", value=f"<@{discord_id}>" if discord_id else "N/A", inline=False)
        embed.add_field(name="Steam Hex", value=steam_hex or "N/A", inline=False)
        embed.add_field(name="FiveM Identifer", value=fivem or "N/A", inline=False)
        embed.add_field(name="Reason", value=reason or "N/A", inline=False)
        embed.add_field(name="Evidence", value=evidence or "N/A", inline=False)
        embed.add_field(name="Warned By", value=warned_by, inline=False)
        embed.add_field(name="Warn Date", value=warn_date, inline=False)

        return embed

    async def start(self):
        """Start the warn browsing session."""
        self.message = await self.interaction.followup.send(embed=self.embed_warn(self.warns[self.current_warn_index]))

        # Add "previous" and "next" reactions
        await self.message.add_reaction("⬅️")
        await self.message.add_reaction("➡️")

        def check(reaction, user):
            """Check if the reaction is valid."""
            return user == self.interaction.user and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == self.message.id

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                if str(reaction.emoji) == "➡️" and self.current_warn_index < len(self.warns) - 1:
                    self.current_warn_index += 1
                    await self.message.edit(embed=self.embed_warn(self.warns[self.current_warn_index]))
                    await self.message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⬅️" and self.current_warn_index > 0:
                    self.current_warn_index -= 1
                    await self.message.edit(embed=self.embed_warn(self.warns[self.current_warn_index]))
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

class findWarn(commands.Cog):
    """A cog to find and display warns."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(
        name='warns',
        description='Find a warn using any identifier',
        force_global=True
    )
    async def _find(
        self, 
        interaction: nextcord.Interaction, 
        identifier: str = nextcord.SlashOption(name="identifier", description="Enter an identifier (Discord ID, Steam Hex, or FiveM ID).", required=True),
    ):
        """Find a warn using an identifier."""
        if nextcord.utils.get(interaction.guild.roles, id=self.db.staffRole()) in interaction.user.roles:
            await interaction.response.defer()

            database = Database()
            warned_users, total_ban_count = self.db.findWarn(identifier)

            if warned_users:
                browser = WarnBrowser(self.bot, interaction, warned_users)
                await browser.start()
            else:
                await interaction.followup.send("No warns found.")
        else:
            await interaction.response.send_message("You are not staff.", ephemeral=True)

def setup(bot: commands.Bot):
    """Set up the cog."""
    bot.add_cog(findWarn(bot))
