import nextcord
from nextcord.ext import commands
from utils.sqlitedatabase import Database

class OnMemberJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()
    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        if self.db.execute(sql="SELECT welcome_system FROM `Welcome System`;", fetch=True)[0][0] == 0:
            return
        else:
            guild = self.bot.get_guild(self.db.execute(sql="SELECT guild_id FROM Config;", fetch=True)[0][0])
            channel = guild.get_channel(self.db.execute(sql="SELECT welcome_channel FROM `Welcome System`;", fetch=True)[0][0])
            message = self.db.execute(sql="SELECT welcome_message FROM `Welcome System`;", fetch=True)[0][0]
            role = guild.get_role(self.db.execute(sql="SELECT welcome_role FROM `Welcome System`;", fetch=True)[0][0])
            image = self.db.execute(sql="SELECT welcome_image FROM `Welcome System`;", fetch=True)[0][0]
            embed = nextcord.Embed(
                title="Welcome!",
                description=message.format(member=member),
                color=nextcord.Color.green(),
                timestamp=nextcord.utils.utcnow(),
            )
            embed.set_image(url=image)
            embed.set_footer(text=f"{member.guild.name}", icon_url=member.guild.icon.url)
            
            await channel.send(embed=embed)
            await member.add_roles(role)

def setup(bot: commands.Bot):
    bot.add_cog(OnMemberJoin(bot))