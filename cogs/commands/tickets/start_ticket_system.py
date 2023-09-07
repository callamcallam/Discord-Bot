import nextcord
from nextcord.ext import commands, application_checks
from utils.sqlitedatabase import Database

db = Database()
staff_role = db.staffRole()

class LockedTicketButtons(nextcord.ui.View): # Locked ticket buttons
    def __init__(self):
        super().__init__(timeout=None)
        self.db = Database()
        self.staff_role = self.db.staffRole()
    
    @nextcord.ui.button(label="Unlock", style=nextcord.ButtonStyle.blurple, custom_id="unlock_ticket", emoji="🔓")
    async def unlock_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        ...
    
    @nextcord.ui.button(label="Transcript", style=nextcord.ButtonStyle.green, custom_id="transcript", emoji="📜")
    async def transcript(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        ...

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red, custom_id="delete_ticket", emoji="🗑️")
    async def delete_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        ...
class TicketControlButtons(nextcord.ui.View): # Ticket control buttons
    def __init__(self):
        super().__init__(timeout=None)
        self.db = Database()
    
    @nextcord.ui.button(label="Lock", style=nextcord.ButtonStyle.blurple, custom_id="lock_ticket", emoji="🔒")
    async def lock_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        staff_role = self.db.staffRole()
        if staff_role not in i.user.roles: return await i.response.send_message("You are not a staff member", ephemeral=True)
        try:
            check = [x for x in self.db.execute(sql="SELECT channel_id FROM `Open Tickets`; ", fetch=True)][0]
            if i.channel.id not in check: return await i.response.send_message(f"This isn't a ticket...")
        except Exception as e:
            await i.response.send_message(f"Error: {e}")
        support_role = self.db.staffRole()
        user = nextcord.utils.get(i.guild.members, id=self.db.execute(sql="SELECT `user-id` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0])
        permissions = {
                i.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                i.guild.me: nextcord.PermissionOverwrite(read_messages=True),
                support_role: nextcord.PermissionOverwrite(read_messages=True),
                i.user: nextcord.PermissionOverwrite(read_messages=True),
                user: nextcord.PermissionOverwrite(read_messages=False)
            }
        await i.channel.edit(permissions=permissions)
        embed = nextcord.Embed(
            title="Ticket Locked!",
            description=f"This ticket has been locked by {i.user.mention}",
            color=nextcord.Color.red(),
            timestamp=i.message.created_at
        )
        embed.set_footer(text="CCRP | Ticket System")
        self.db.execute(sql="UPDATE `Open Tickets` SET `is-locked` = (?) WHERE `channel_id` = (?)", values=("1", i.channel.id), fetch=False, commit=True)
        await i.response.send_message(embed=embed, ephemeral=False, view=LockedTicketButtons())

    @nextcord.ui.button(label="Claim", style=nextcord.ButtonStyle.green, custom_id="claim_ticket", emoji="🛄")
    #@application_checks.has_role(int(staff_role))
    async def claim_ticket(self, button: nextcord.ui.Button,i: nextcord.Interaction):
        staff_role = self.db.staffRole()
        if staff_role not in i.user.roles: return await i.response.send_message("You are not a staff member", ephemeral=True)
        user_id = self.db.execute(sql="SELECT `user-id` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0]
        user = nextcord.utils.get(i.guild.members, id=user_id)
        if user is None: return await i.response.send_message("The user is not in the server anymore", ephemeral=True)
        support_role = self.db.staffRole()
        self.db.execute(sql="UPDATE `Open Tickets` SET `claimed-by` = (?) WHERE `channel_id` = (?)", values=(i.user.id, i.channel.id), fetch=False, commit=True)
        await i.channel.edit(topic=f"Claimed by {i.user.name}")
        await i.response.send_message(f"{i.user.mention} has claimed this ticket!", ephemeral=False)
    
    @nextcord.ui.button(label="Close", style=nextcord.ButtonStyle.red, custom_id="close_ticket", emoji="🔒")
    async def close_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        staff_role = self.db.staffRole()
        if staff_role not in i.user.roles: return await i.response.send_message("You are not a staff member", ephemeral=True)
        user_id = self.db.execute(sql="SELECT `user-id` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0]
        user = nextcord.utils.get(i.guild.members, id=user_id)
        if user is None: return await i.response.send_message("The user is not in the server anymore", ephemeral=True)
        support_role = self.db.staffRole()
        if self.db.execute(sql="SELECT `transcripts` FROM `Ticket System`;", fetch=True)[0][0] == "1":
            
            await i.channel.send(file=nextcord.File(f"transcripts/{i.channel.name}.txt"))
        self.db.execute(sql="DELETE FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=False, commit=True)

    

class OpenTicketDropDown(nextcord.ui.View): # Open a ticket here.
    def __init__(self, *, timeout: float | None = None, auto_defer: bool = True) -> None:
        super().__init__(timeout=timeout, auto_defer=auto_defer)
        self.db = Database()


    @nextcord.ui.select(
        placeholder="Select a reason for your ticket",
        options=[
            nextcord.SelectOption(label="General Support", value="general-support"),
            nextcord.SelectOption(label="Donation", value="donation"),
            nextcord.SelectOption(label="Ban Appeal", value="ban"),
        ],
        min_values=1,
        max_values=1,
        custom_id="ticket_reason"
    )
    async def ticket_reasonc(self, select: nextcord.ui.Select, interaction: nextcord.Interaction):
        if select.values[0] == "general-support":
            support_category = nextcord.utils.get(interaction.guild.categories, id=int(self.db.execute(sql="SELECT support_category FROM `Ticket System`;", fetch=True)[0][0]))
            if support_category is None: return await interaction.response.send_message("The general support category is not set. Please set it", ephemeral=True)
            support_role = nextcord.utils.get(interaction.guild.roles, id=int(self.db.execute(sql="SELECT support_role FROM `Ticket System`;", fetch=True)[0][0]))
            if support_role is None: return await interaction.response.send_message("The support role is not set. Please set it", ephemeral=True)
            general_support_welcome_message = self.db.execute(sql="SELECT support_welcome_message FROM `Ticket System`;", fetch=True)[0][0]
            permissions = {
                interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
                support_role: nextcord.PermissionOverwrite(read_messages=True),
                interaction.user: nextcord.PermissionOverwrite(read_messages=True),

            }
            gen_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}", category=support_category, overwrites=permissions)
            self.db.execute(sql="INSERT INTO `Open Tickets` (uuid, `user-id`, `ticket-type`, channel_id, `is-locked`) VALUES (?, ?, ?, ?, ?)", values=(self.db.randID(), interaction.user.id, "general-support", gen_channel.id, "0"), fetch=False, commit=True)
            embed = nextcord.Embed(
                title="Ticket Opened!",
                description=general_support_welcome_message.format(member=interaction.user),
                color=nextcord.Color.green()
            )
            embed.set_footer(text="CCRP | Ticket System")
            await gen_channel.send(content=f"{interaction.user.mention}", delete_after=1)
            await gen_channel.send(embed=embed, view=TicketControlButtons())
            await interaction.response.send_message(f"Your ticket has been opened in {gen_channel.mention}", ephemeral=True)
        elif select.values[0] == "donation":
            donation_category = nextcord.utils.get(interaction.guild.categories, id=int(self.db.execute(sql="SELECT donation_category FROM `Ticket System`;", fetch=True)[0][0]))
            if donation_category is None: return await interaction.response.send_message("The donation category is not set. Please set it", ephemeral=True)
            support_role = nextcord.utils.get(interaction.guild.roles, id=int(self.db.execute(sql="SELECT support_role FROM `Ticket System`;", fetch=True)[0][0]))
            if support_role is None: return await interaction.response.send_message("The support role is not set. Please set it", ephemeral=True)
            donation_welcome_message = self.db.execute(sql="SELECT donation_welcome_message FROM `Ticket System`;", fetch=True)[0][0]
            permissions = {
                interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
                support_role: nextcord.PermissionOverwrite(read_messages=True),
                interaction.user: nextcord.PermissionOverwrite(read_messages=True),

            }

            don_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}", category=donation_category, overwrites=permissions)
            self.db.execute(sql="INSERT INTO `Open Tickets` (uuid, `user-id`, `ticket-type`, channel_id, `is-locked`) VALUES (?, ?, ?, ?, ?)", values=(self.db.randID(), interaction.user.id, "donation", don_channel.id, "0"), fetch=False, commit=True)
            embed = nextcord.Embed(
                title="Ticket Opened!",
                description=donation_welcome_message.format(member=interaction.user),
            )
            embed.set_footer(text="CCRP | Ticket System")
            await don_channel.send(embed=embed, view=TicketControlButtons())
            await interaction.response.send_message(f"Your ticket has been opened in {don_channel.mention}", ephemeral=True)

        elif select.values[0] == "ban":
            ban_appeal_category = nextcord.utils.get(interaction.guild.categories, id=int(self.db.execute(sql="SELECT ban_appeal_category FROM `Ticket System`;", fetch=True)[0][0]))
            if ban_appeal_category is None: return await interaction.response.send_message("The ban appeal category is not set. Please set it", ephemeral=True)
            support_role = nextcord.utils.get(interaction.guild.roles, id=int(self.db.execute(sql="SELECT support_role FROM `Ticket System`;", fetch=True)[0][0]))
            if support_role is None: return await interaction.response.send_message("The support role is not set. Please set it", ephemeral=True)
            ban_appeal_welcome_message = self.db.execute(sql="SELECT ban_appeal_welcome_message FROM `Ticket System`;", fetch=True)[0][0]
            permissions = {
                interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
                support_role: nextcord.PermissionOverwrite(read_messages=True),
                interaction.user: nextcord.PermissionOverwrite(read_messages=True),

            }
            ban_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}", category=ban_appeal_category, overwrites=permissions)
            self.db.execute(sql="INSERT INTO `Open Tickets` (uuid, `user-id`, `ticket-type`, channel_id, `is-locked`) VALUES (?, ?, ?, ?, ?)", values=(self.db.randID(), interaction.user.id, "ban", ban_channel.id, "0"), fetch=False, commit=True)
            embed = nextcord.Embed(
                title="Ticket Opened!",
                description=ban_appeal_welcome_message.format(member=interaction.user),
            )
            embed.set_footer(text="CCRP | Ticket System")
            await ban_channel.send(embed=embed, view=TicketControlButtons())
            await interaction.response.send_message(f"Your ticket has been opened in {ban_channel.mention}", ephemeral=True)

class OpenTicketOpenButton(nextcord.ui.View): # Open discord ticket button
    def __init__(self):
        super().__init__(timeout=None)
        self.db = Database()

    @nextcord.ui.button(label="Open a ticket!", style=nextcord.ButtonStyle.green, custom_id="open_ticket", emoji="🎟️")
    async def open_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        await i.response.send_message("In order to open a ticket, please select a category", ephemeral=True, view=OpenTicketDropDown())



class StartTicketSystem(commands.Cog): # Start Ticket System
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(name="start-ticket-system", description="Start the ticket system", force_global=True)
    @application_checks.has_guild_permissions(manage_guild=True)
    async def _start_ticket_system(self, i: nextcord.Interaction):
        ticket_channel = nextcord.utils.get(i.guild.channels, id=int(self.db.execute(sql="SELECT ticket_channel FROM `Ticket System`;", fetch=True)[0][0]))
        if ticket_channel is None: await i.response.send_message("The ticket channel is not set. Please set it", ephemeral=True)
        support_role = nextcord.utils.get(i.guild.roles, id=int(self.db.execute(sql="SELECT support_role FROM `Ticket System`;", fetch=True)[0][0]))
        if support_role is None: await i.response.send_message("The support role is not set. Please set it", ephemeral=True)
        embed = nextcord.Embed(
            title="Open a ticket!",
            description="React with 🎟️ to open a ticket",
            color=nextcord.Color.green(),
            
        )
        embed.set_footer(text="CCRP | Ticket System")
        await ticket_channel.send(embed=embed, view=OpenTicketOpenButton())
        await i.response.send_message("The ticket system has been started!", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(StartTicketSystem(bot))
