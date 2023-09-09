import nextcord
from nextcord import SlashOption
from nextcord.ext import commands
from utils.sqlitedatabase import Database
from nextcord.ext import application_checks
class SetConfig(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()
    
    @nextcord.slash_command(name="set_config", description="Set a config value") # ✅
    @application_checks.has_permissions(administrator=True)
    async def set_config(self, interaction: nextcord.Interaction):
        pass
    

    @set_config.subcommand(name="prefix", description="Set the bot's prefix") # ✅
    @application_checks.has_permissions(administrator=True)
    async def set_prefix(self, interaction: nextcord.Interaction, prefix: str):
        if self.db.execute(sql="SELECT command_prefix FROM Config;", fetch=True)[0][0] == prefix:
            await interaction.response.send_message(content="The prefix is already set to that!", ephemeral=True)
            return
        self.db.execute(sql="UPDATE Config SET command_prefix = ?;", values=(prefix,), commit=True)
        await interaction.response.send_message(content=f"The prefix has been set to `{prefix}`!", ephemeral=True)
        

    @set_config.subcommand(name="token", description="Set the bot's token") # ✅
    @application_checks.has_permissions(administrator=True)
    async def set_token(self, interaction: nextcord.Interaction, token: str):
        if self.db.execute(sql="SELECT token FROM Config;", fetch=True)[0][0] == token:
            await interaction.response.send_message(content="The prefix is already set to that!", ephemeral=True)
            return
        self.db.execute(sql="UPDATE Config SET token = ?;", values=(token,), commit=True)
        await interaction.response.send_message(content=f"The token has been set to `{token}`!", ephemeral=True)
        
    @set_config.subcommand(name="status", description="Set the bot's status") # ✅
    @application_checks.has_permissions(administrator=True)
    async def set_status(self, interaction: nextcord.Interaction, status: str, activity_type: str = SlashOption(description="The type of activity", choices=["playing", "listening", "watching", "competing"])):
        #await interaction.channel.send(status)
        new_status = None
        if self.db.execute(sql="SELECT status FROM Config;", fetch=True)[0][0] == status:
            await interaction.response.send_message(content="The status is already set to that!", ephemeral=True)
            return
        if activity_type == "playing":
            new_status = nextcord.Game(name=status)
        elif  activity_type == "listening":
            new_status = nextcord.Activity(type=nextcord.ActivityType.listening, name=status)
        elif activity_type == "watching":
            new_status = nextcord.Activity(type=nextcord.ActivityType.watching, name=status)
        elif activity_type == "competing":
            new_status = nextcord.Activity(type=nextcord.ActivityType.competing, name=status)
        elif activity_type == None:
            new_status = nextcord.Game(name=status)
        await self.bot.change_presence(activity=new_status)
        self.db.execute(sql="UPDATE Config SET status = ?;", values=(status,), commit=True)
        self.db.execute(sql="UPDATE Config SET status_type = ?;", values=(activity_type,), commit=True)
        await interaction.response.send_message(content=f"The status has been set to `{status}`!", ephemeral=True)
    


def setup(bot: commands.Bot):
    bot.add_cog(SetConfig(bot))