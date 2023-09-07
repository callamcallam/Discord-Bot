import nextcord
from nextcord.ext import commands, application_checks
from utils.sqlitedatabase import Database


class SetLeave(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()
    
    @nextcord.slash_command(name="set-leave", description="Sets the leave system up for the server.", force_global=True)
    @application_checks.has_permissions(manage_guild=True)
    async def callback(self, i: nextcord.Interaction, option: str = nextcord.SlashOption(name="option", description="Select an option!", choices=["Active", "Channel", "Message", "Image URL"], required=True), active: str = nextcord.SlashOption(name="active", description="Enable/Disable Leave System!", choices=["Enable", "Disable"], required=False), channel: nextcord.TextChannel = None, message: str = None, image_url: str = None, role: nextcord.Role = None):
        if option == "Active":
            if active.lower() == "enable":
                if self.db.execute(sql="SELECT `leave_system` FROM `Leave System`;", fetch=True)[0][0] == 0:
                    self.db.execute(sql="UPDATE `Leave System` SET `leave_system` = ?;", values=(1,), commit=True)
                    await i.response.send_message(content="The Leave System has been enabled!", ephemeral=True)
                elif self.db.execute(sql="SELECT `leave_system` FROM `Leave System`;", fetch=True)[0][0] == 1:
                    await i.response.send_message(content="The Leave System is already enabled!", ephemeral=True)
            elif active.lower() == "disable":
                if self.db.execute(sql="SELECT `leave_system` FROM `Leave System`", fetch=True)[0][0] == 1:
                    self.db.execute(sql="UPDATE `Leave System` SET `leave_system` = ?;", values=(0,), commit=True)
                    await i.response.send_message(content="The Leave System has been disabled!", ephemeral=True)
                elif self.db.execute(sql="SELECT `leave_system` FROM `Leave System`;", fetch=True)[0][0] == 0:
                    await i.response.send_message(content="The Leave System is already disabled!", ephemeral=True)
        elif option == "Channel":
            if self.db.execute(sql="SELECT `leave_system` FROM `Leave System`;", fetch=True)[0][0] == 1:
                if channel.id == self.db.execute(sql="SELECT `leave_channel` FROM `Leave System`;", fetch=True)[0][0]:
                    await i.response.send_message(content="The leave channel is already set to this channel!", ephemeral=True)
                    return
                elif channel is None:
                    await i.response.send_message(content="Please provide a channel!", ephemeral=True)
                else:
                    self.db.execute(sql="UPDATE `Leave System` SET `leave_channel` = ?;", values=(channel.id,), commit=True)
                    await i.response.send_message(content=f"The leave channel has been set to {channel.mention}!", ephemeral=True)
            else:
                await i.response.send_message(content="The Leave System is not enabled!", ephemeral=True)
        elif option == "Message":
            if self.db.execute(sql="SELECT `leave_system` FROM `Leave System`;", fetch=True)[0][0] == 1:
                if message is None:
                    await i.response.send_message(content="Please provide a message!", ephemeral=True)
                else:
                    self.db.execute(sql="UPDATE `Leave System` SET `leave_message` = ?;", values=(message,), commit=True)
                    await i.response.send_message(content=f"The welcome message has been set to {message}!", ephemeral=True)
            else:
                await i.response.send_message(content="The Leave System is not enabled!", ephemeral=True)
        elif option == "Image URL":
            if self.db.execute(sql="SELECT `leave_system` FROM `Leave System`;", fetch=True)[0][0] == 1:
                if image_url is None:
                    await i.response.send_message(content="Please provide an image URL!", ephemeral=True)
                else:
                    self.db.execute(sql="UPDATE `Leave System` SET `leave_image` = ?;", values=(image_url,), commit=True)
                    await i.response.send_message(content=f"The welcome image has been set to {image_url}!", ephemeral=True)
            else:
                await i.response.send_message(content="The Leave System is not enabled!", ephemeral=True)
    
def setup(bot: commands.Bot):
    bot.add_cog(SetLeave(bot))    
