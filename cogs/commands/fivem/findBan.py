import nextcord, asyncio
from nextcord.ext import commands
from utils.sqlitedatabase import Database 
from typing import Optional

class BanBrowser:
    """A class to browse through bans interactively."""
    def __init__(self, bot, interaction, bans):
        self.bot = bot
        self.interaction = interaction
        self.bans = bans
        self.current_ban_index = 0
        self.message = None

    def embed_ban(self, ban):
        """Create an embed for a specific ban."""
        discord_id, steam_hex, fivem, evidence, reason, banned_by, ban_duration, ban_date, banned_user = ban

        embed = nextcord.Embed(
            title=f"Ban {self.current_ban_index + 1}/{len(self.bans)}",
            description="Details of the ban.",
            color=nextcord.Color.red()
        )

        # Add fields to the embed for each piece of ban information
        embed.add_field(name="Banned User", value=banned_user or "N/A", inline=False)
        embed.add_field(name="Discord ID", value=f"<@{discord_id}>" if discord_id else "N/A", inline=False)
        embed.add_field(name="Steam Hex", value=steam_hex or "N/A", inline=False)
        embed.add_field(name="FiveM Identifer", value=fivem or "N/A", inline=False)
        embed.add_field(name="Reason", value=reason or "N/A", inline=False)
        embed.add_field(name="Evidence", value=evidence or "N/A", inline=False)
        embed.add_field(name="Ban Duration", value=ban_duration or "N/A", inline=False)
        embed.add_field(name="Banned By", value=banned_by, inline=False)
        embed.add_field(name="Ban Date", value=ban_date, inline=False)

        return embed

    async def start(self):
        """Start the ban browsing session."""
        self.message = await self.interaction.followup.send(embed=self.embed_ban(self.bans[self.current_ban_index]))

        # Add "previous" and "next" reactions
        await self.message.add_reaction("⬅️")
        await self.message.add_reaction("➡️")

        def check(reaction, user):
            """Check if the reaction is valid."""
            return user == self.interaction.user and str(reaction.emoji) in ["⬅️", "➡️"] and reaction.message.id == self.message.id

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                if str(reaction.emoji) == "➡️" and self.current_ban_index < len(self.bans) - 1:
                    self.current_ban_index += 1
                    await self.message.edit(embed=self.embed_ban(self.bans[self.current_ban_index]))
                    await self.message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "⬅️" and self.current_ban_index > 0:
                    self.current_ban_index -= 1
                    await self.message.edit(embed=self.embed_ban(self.bans[self.current_ban_index]))
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

class findBan(commands.Cog):
    """A cog to find and display bans."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(
        name='bans',
        description='Find a ban using any identifier',
        force_global=True
    )
    async def _find(self, interaction: nextcord.Interaction, identifier: str = nextcord.SlashOption(name="identifier", description="Enter an identifier (Discord ID, Steam Hex, or FiveM ID).", required=True)):
        """Find a ban using an identifier."""
        if nextcord.utils.get(interaction.guild.roles, id=int(self.db.execute(sql="SELECT `support_role` FROM `Ticket System`;")[0][0])) in interaction.user.roles:
            await interaction.response.defer()

            database = Database()
            banned_users, total_ban_count = database.findBan(identifier)

            if banned_users:
                browser = BanBrowser(self.bot, interaction, banned_users)
                await browser.start()
            else:
                await interaction.followup.send("No bans found.")
        else:
            await interaction.response.send_message("You are not staff.", ephemeral=True)

def setup(bot: commands.Bot):
    """Set up the cog."""
    bot.add_cog(findBan(bot))
