import nextcord
from nextcord.ext import commands
from utils.sqlitedatabase import Database

class SetWelcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()
    
    @nextcord.slash_command(name="set-welcome", description="Sets the welcome channel for the server.")
    async def callback(self, i: nextcord.Interaction, option: nextcord.SlashOption(name="Select an Option!", description="Setup the welcome system.", choices=["Active", "Channel", "Message", "Image URL", "Role"], required=True), active: nextcord.SlashOption(name="Enable/Disable Welcome System", choices=["Enable", "Disable"], required=False), channel: nextcord.TextChannel = None, message: str = None, image_url: str = None, role: nextcord.Role = None):
        if option == "Active":
            if active.lower() == "enable":
                if self.db.execute(sql="SELECT `welcome_system` FROM `Welcome System`;", fetch=True)[0][0] == 0:
                    self.db.execute(sql="UPDATE `Welcome System` SET `welcome_system` = ?;", values=(1,), commit=True)
                    await i.response.send_message(content="The welcome system has been enabled!", ephemeral=True)
                elif self.db.execute(sql="SELECT `welcome_system` FROM `Welcome System`;", fetch=True)[0][0] == 1:
                    await i.response.send_message(content="The welcome system is already enabled!", ephemeral=True)
            elif active.lower() == "disable":
                if self.db.execute(sql="SELECT `welcome_system FROM `Welcome System", fetch=True)[0][0] == 1:
                    self.db.execute(sql="UPDATE `Welcome System` SET `welcome_system` = ?;", values=(0,), commit=True)
                    await i.response.send_message(content="The welcome system has been disabled!", ephemeral=True)
                elif self.db.execute(sql="SELECT `welcome_system` FROM `Welcome System`;", fetch=True)[0][0] == 0:
                    await i.response.send_message(content="The welcome system is already disabled!", ephemeral=True)
        elif option == "Channel":
            if self.db.execute(sql="SELECT `welcome_system` FROM `Welcome System`;", fetch=True)[0][0] == 1:
                if channel.id == self.db.execute(sql="SELECT `welcome_channel` FROM `Welcome System`;", fetch=True)[0][0]:
                    await i.response.send_message(content="The welcome channel is already set to this channel!", ephemeral=True)
                    return
                elif channel is None:
                    await i.response.send_message(content="Please provide a channel!", ephemeral=True)
                else:
                    self.db.execute(sql="UPDATE `Welcome System` SET `welcome_channel` = ?;", values=(channel.id,), commit=True)
                    await i.response.send_message(content=f"The welcome channel has been set to {channel.mention}!", ephemeral=True)
            else:
                await i.response.send_message(content="The welcome system is not enabled!", ephemeral=True)
        elif option == "Message":
            if self.db.execute(sql="SELECT `welcome_system` FROM `Welcome System`;", fetch=True)[0][0] == 1:
                if message is None:
                    await i.response.send_message(content="Please provide a message!", ephemeral=True)
                else:
                    self.db.execute(sql="UPDATE `Welcome System` SET `welcome_message` = ?;", values=(message,), commit=True)
                    await i.response.send_message(content=f"The welcome message has been set to {message}!", ephemeral=True)
            else:
                await i.response.send_message(content="The welcome system is not enabled!", ephemeral=True)
        elif option == "Image URL":
            if self.db.execute(sql="SELECT `welcome_system` FROM `Welcome System`;", fetch=True)[0][0] == 1:
                if image_url is None:
                    await i.response.send_message(content="Please provide an image URL!", ephemeral=True)
                else:
                    self.db.execute(sql="UPDATE `Welcome System` SET `welcome_image` = ?;", values=(image_url,), commit=True)
                    await i.response.send_message(content=f"The welcome image has been set to {image_url}!", ephemeral=True)
            else:
                await i.response.send_message(content="The welcome system is not enabled!", ephemeral=True)
        elif option == "Role":
            if self.db.execute(sql="SELECT `welcome_system` FROM `Welcome System`;", fetch=True)[0][0] == 1:
                if role.id == self.db.execute(sql="SELECT `welcome_role` FROM `Welcome System`;", fetch=True)[0][0]:
                    await i.response.send_message(content="The welcome role is already set to this role!", ephemeral=True)
                    return
                elif role is None:
                    await i.response.send_message(content="Please provide a role!", ephemeral=True)
                else:
                    self.db.execute(sql="UPDATE `Welcome System` SET `welcome_role` = ?;", values=(role.id,), commit=True)
                    await i.response.send_message(content=f"The welcome role has been set to {role.mention}!", ephemeral=True)
            else:
                await i.response.send_message(content="The welcome system is not enabled!", ephemeral=True)
