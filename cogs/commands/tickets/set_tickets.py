import nextcord
from nextcord.ext import commands, application_checks
from utils.sqlitedatabase import Database

class SetTickets(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(name="set-tickets", description="Set the ticket category and log channel", force_global=True)
    @application_checks.has_permissions(manage_guild=True)
    async def tickets(self, i: nextcord.Interaction, option: str = nextcord.SlashOption(name="enable", choices=["Enable", "Disable"], required=True)):
        if option == "Enable":
            if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 0: 
                self.db.execute(sql="UPDATE `Ticket System` SET `ticket_system` = 1;")
                await i.response.send_message("Ticket System Enabled", ephemeral=True)
            else:
                await i.response.send_message("Ticket System is already enabled", ephemeral=True)
        elif option == "Disable":
            if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 1: 
                self.db.execute(sql="UPDATE `Ticket System` SET `ticket_system` = 0;")
                await i.response.send_message("Ticket System Disabled", ephemeral=True)
            else:
                await i.response.send_message("Ticket System is already disabled", ephemeral=True)
    
    @tickets.subcommand(name="ticket-channel", description="Channel where the ticket will be opened.")
    @application_checks.has_permissions(manage_guild=True)
    async def ticket_channel(self, i: nextcord.Interaction, channel: nextcord.TextChannel = None):
        if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 0:
            return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
        if self.db.execute(sql="SELECT `ticket_channel` FROM `Ticket System`;", fetch=True)[0][0] == channel.id:
            return await i.response.send_message("This is already the ticket channel.", ephemeral=True)
        self.db.execute(sql="UPDATE `Ticket System` SET `ticket_channel` = ?;", values=(channel.id,), commit=True)
        return await i.response.send_message(f"Ticket Channel Set to: {channel.mention}", ephemeral=True)
        
    @tickets.subcommand(name="general-support-setup", description="Setup general support tickets")
    @application_checks.has_permissions(manage_guild=True)
    async def general(self, i: nextcord.Interaction, option: str = nextcord.SlashOption(name="options", choices=["Support Catergory", "Welcome Message", "Claim Message", "Close Message"], required=True), category: nextcord.CategoryChannel= None, welcome: str = None, claim: str= None, close: str= None):
        if option == "Support Catergory":
            if self.db.execute(sql="SELECT `support_category` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if int(self.db.execute(sql="SELECT `support_category` FROM `Ticket System`;", fetch=True)[0][0]) == category.id:
                return await i.response.send_message("This is already the general support category.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `support_category` = ?;", values=(category.id,))
            return await i.response.send_message(f"General Support Category Set to: {category}", ephemeral=True)
        elif option == "Welcome Message":
            if self.db.execute(sql="SELECT `support_category` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if self.db.execute(sql="SELECT `support_welcome_message` FROM `Ticket System`;", fetch=True)[0][0] == welcome.id:
                return await i.response.send_message("This is already the general support welcome message.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `support_welcome_message` = ?;", values=(welcome.id,))
            return i.response.send_message(f"General Support Welcome Message Set to: {welcome}", ephemeral=True)
        elif option == "Claim Message":
            if self.db.execute(sql="SELECT `support_category` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if self.db.execute(sql="SELECT `support_claim_message` FROM `Ticket System`;", fetch=True)[0][0] == claim.id:
                return await i.response.send_message("This is already the general support claim message.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `support_claim_message` = ?;", values=(claim.id,))
            return await i.response.send_message(f"General Support Claim Message Set to: {claim}", ephemeral=True)
        elif option == "Close Message":
            if self.db.execute(sql="SELECT `support_category` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if self.db.execute(sql="SELECT `support_close_message` FROM `Ticket System`;", fetch=True)[0][0] == close.id:
                return await i.response.send_message("This is already the general support close message.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `support_close_message` = ?;", values=(close.id,))
            return i.response.send_message(f"General Support Close Message Set to: {close}", ephemeral=True)
        

    @tickets.subcommand(name="donation-setup", description="Setup donation tickets")
    @application_checks.has_permissions(manage_guild=True)
    async def donation(self, i: nextcord.Interaction, option: str = nextcord.SlashOption(name="options", choices=["Donation Catergory", "Welcome Message", "Claim Message", "Close Message"], required=True), category: nextcord.CategoryChannel= None, welcome: str = None, claim: str= None, close: str= None):
        if option == "Donation Catergory":
            if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if int(self.db.execute(sql="SELECT `donation_category` FROM `Ticket System`;", fetch=True)[0][0]) == category.id:
                return await i.response.send_message("This is already the donation category.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `donation_category` = ?;", values=(category.id,))
            return await i.response.send_message(f"Donation Category Set to: {category}", ephemeral=True)
        elif option == "Welcome Message":
            if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if self.db.execute(sql="SELECT `donation_welcome_message` FROM `Ticket System`;", fetch=True)[0][0] == welcome.id:
                return await i.response.send_message("This is already the donation welcome message.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `donation_welcome_message` = ?;", values=(welcome.id,))
            return i.response.send_message(f"Donation Welcome Message Set to: {welcome}", ephemeral=True)
        elif option == "Claim Message":
            if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if self.db.execute(sql="SELECT `donation_claim_message` FROM `Ticket System`;", fetch=True)[0][0] == claim.id:
                return await i.response.send_message("This is already the donation claim message.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `donation_claim_message` = ?;", values=(claim.id,))
            return i.response.send_message(f"Donation Claim Message Set to: {claim}", ephemeral=True)
        elif option == "Close Message":
            if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if self.db.execute(sql="SELECT `donation_close_message` FROM `Ticket System`;", fetch=True)[0][0] == close.id:
                return i.response.send_message("This is already the donation close message.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `donation_close_message` = ?;", values=(close.id,))
            return await i.response.send_message(f"Donation Close Message Set to: {close}", ephemeral=True)
        

    @tickets.subcommand(name="ban-appeal-setup", description="Setup ban appeal tickets")
    @application_checks.has_permissions(manage_guild=True)
    async def ban(self, i: nextcord.Interaction, option: str = nextcord.SlashOption(name="options", choices=["Ban Appeal Catergory", "Welcome Message", "Claim Message", "Close Message"], required=True), category: nextcord.CategoryChannel= None, welcome: str = None, claim: str= None, close: str= None):
        if option == "Ban Appeal Catergory":
            if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if int(self.db.execute(sql="SELECT `ban_category` FROM `Ticket System`;", fetch=True)[0][0]) == category.id:
                return await i.response.send_message("This is already the ban appeal category.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `ban_category` = ?;", values=(category.id,))
            return await i.response.send_message(f"Ban Appeal Category Set to: {category}", ephemeral=True)
        elif option == "Welcome Message":
            if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if self.db.execute(sql="SELECT `ban_welcome_message` FROM `Ticket System`;", fetch=True)[0][0] == welcome.id:
                return await i.response.send_message("This is already the ban appeal welcome message.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `ban_welcome_message` = ?;", values=(welcome.id,))
            return i.response.send_message(f"Ban Appeal Welcome Message Set to: {welcome}", ephemeral=True)
        elif option == "Claim Message":
            if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if self.db.execute(sql="SELECT `ban_claim_message` FROM `Ticket System`;", fetch=True)[0][0] == claim.id:
                return await i.response.send_message("This is already the ban appeal claim message.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `ban_claim_message` = ?;", values=(claim.id,))
            return i.response.send_message(f"Ban Appeal Claim Message Set to: {claim}", ephemeral=True)
        elif option == "Close Message":
            if self.db.execute(sql="SELECT `ticket_system` FROM `Ticket System`;", fetch=True)[0][0] == 0:
                return await i.response.send_message("Ticket System Disabled. Please enable it first.", ephemeral=True)
            if self.db.execute(sql="SELECT `ban_close_message` FROM `Ticket System`;", fetch=True)[0][0] == close.id:
                return await i.response.send_message("This is already the ban appeal close message.", ephemeral=True)
            self.db.execute(sql="UPDATE `Ticket System` SET `ban_close_message` = ?;", values=(close.id,))
            return await i.response.send_message(f"Ban Appeal Close Message Set to: {close}", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(SetTickets(bot))