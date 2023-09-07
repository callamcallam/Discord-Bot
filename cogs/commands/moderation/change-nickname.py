import nextcord
from nextcord.ext import commands
from utils.sqlitedatabase import Database

class ChangeNickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
    
    @nextcord.slash_command(name="change-nick", description="Change a user's nickname.", force_global=True)
    @commands.has_permissions(manage_nicknames=True)
    async def changenickname(self, i: nextcord.Interaction, member: nextcord.Member, nickname: str):
        await member.edit(nick=nickname)
        await i.response.send_message(f"Changed {member.mention}'s nickname to {nickname}.")


def setup(bot):
    bot.add_cog(ChangeNickname(bot))