import nextcord, os, datetime, asyncio
from dateutil.relativedelta import relativedelta
from nextcord.ext import commands, application_checks
from utils.sqlitedatabase import Database

debug = True
db = Database()
staff_role = db.staffRole()


class LockedTicketButtons(nextcord.ui.View): # Locked ticket buttons
    def __init__(self, bot:commands.Bot):
        super().__init__(timeout=None)
        self.db = Database()
        self.bot = bot
        #self.staff_role = nextcord.utils.get(i.guild.roles,id=self.db.staffRole())
    
    @nextcord.ui.button(label="Unlock", style=nextcord.ButtonStyle.blurple, custom_id="unlock_ticket", emoji="🔓")
    async def unlock_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        user_embed = nextcord.Embed(
            title="Ticket Unlocked!",
            description=f"Your ticket has been unlocked by {i.user.mention}",
            color=nextcord.Color.green(),
            timestamp=i.message.created_at
        )
        user_embed.set_footer(text="CCRP | Ticket System")
        staff_role = nextcord.utils.get(i.guild.roles,id=self.db.staffRole())
        if staff_role not in i.user.roles: return await i.response.send_message("You are not a staff member", ephemeral=True)
        try: 
            check = int(self.db.execute(sql="SELECT `channel_id` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0])
            if i.channel.id != check: return await i.response.send_message(f"This isn't a ticket...")
        except Exception as e:
            await i.response.send_message(f"Error: {e}")
        check2 = int(self.db.execute(sql="SELECT `is-locked` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0])
        if check2 == 0: return await i.response.send_message("This ticket is already unlocked", ephemeral=True)
        support_role = self.db.staffRole()
        user = nextcord.utils.get(i.guild.members, id=self.db.execute(sql="SELECT `user-id` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0])
        permissions = {
                i.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                i.guild.me: nextcord.PermissionOverwrite(read_messages=True),
                support_role: nextcord.PermissionOverwrite(read_messages=True),
                i.user: nextcord.PermissionOverwrite(read_messages=True),
        }
        self.db.execute(sql="UPDATE `Open Tickets` SET `is-locked` = (?) WHERE `channel_id` = (?)", values=(0, i.channel.id), fetch=False, commit=True)
        await i.channel.edit(permissions=permissions)
        embed = nextcord.Embed(
            title="Ticket Unlocked!",
            description=f"This ticket has been unlocked by {i.user.mention}",
            color=nextcord.Color.green(),
            timestamp=i.message.created_at
        )
        embed.set_footer(text="CCRP | Ticket System")
        await user.send(embed=user_embed)
        await i.response.send_message(embed=embed, ephemeral=False, view=TicketControlButtons(self.bot))
    
    @nextcord.ui.button(label="Transcript", style=nextcord.ButtonStyle.green, custom_id="transcript", emoji="📜")
    async def transcript(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        ...

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red, custom_id="delete_ticket", emoji="🗑️")
    async def delete_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        ...
        
class TicketControlButtons(nextcord.ui.View):
    """
    A class that represents the ticket control buttons view.

    Attributes:
    bot (commands.Bot): The bot instance.
    db (Database): The database instance.
    """

    def __init__(self, bot: commands.Bot):
        """
        Initializes the TicketControlButtons class.

        Args:
        bot (commands.Bot): The bot instance.
        """
        super().__init__(timeout=None)
        self.bot = bot
        self.db = Database()

    @nextcord.ui.button(label="Lock", style=nextcord.ButtonStyle.blurple, custom_id="lock_ticket", emoji="🔒")
    async def lock_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        """
        A coroutine that locks the ticket and updates the database.

        Args:
        button (nextcord.ui.Button): The lock button.
        i (nextcord.Interaction): The interaction object.
        """
        staff_role = nextcord.utils.get(i.guild.roles,id=self.db.staffRole())
        if staff_role not in i.user.roles: return await i.response.send_message("You are not a staff member", ephemeral=True)
        try:
            try:
                
                check = int(self.db.execute(sql="SELECT `channel_id` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0])
                if i.channel.id != check: return await i.response.send_message(f"This isn't a ticket...")
            except Exception as e:
                if debug: raise e
                await i.response.send_message(f"Ticket not found!")
            try:
                
                check2 = int(self.db.execute(sql="SELECT `is-locked` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0])
                if check2 == 1: return await i.response.send_message("This ticket is already locked", ephemeral=True)
            except Exception as e:
                if debug: raise e
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
            user_embed = nextcord.Embed(
                title="Ticket Locked!",
                description=f"Your ticket has been locked.",
                color=nextcord.Color.red(),
                timestamp=i.message.created_at
                
            )
            user_embed.set_footer(text="CCRP | Ticket System")
            user_embed.add_field(name="🔒 Locked by", value=i.user.mention)
            user_embed.add_field(name="📝 Ticket Type", value=self.db.execute(sql="SELECT `ticket-type` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0])
            user_embed.add_field(name="📅 Date", value=i.message.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
            user_embed.add_field(name="💁‍♂️ Claimed by", value=nextcord.utils.get(i.guild.members, id=self.db.execute(sql="SELECT `claimed-by` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0]).mention)
            user_embed.add_field(name="🗝️ UUID", value=self.db.execute(sql="SELECT `uuid` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0])
            await user.send(embed=user_embed)
            try:
                
                self.db.execute(sql="UPDATE `Open Tickets` SET `is-locked` = (?) WHERE `channel_id` = (?)", values=(1, i.channel.id), fetch=False, commit=True)
            except Exception as e:
                return await i.response.send_message(f"Error: {e}")
            
            await i.response.send_message(embed=embed, ephemeral=False, view=LockedTicketButtons(self.bot))
        except Exception as e:
            if debug: raise e
            else:
                return await i.response.send_message(f"An error occured, please contact the owner.")

    @nextcord.ui.button(label="Claim", style=nextcord.ButtonStyle.green, custom_id="claim_ticket", emoji="🛄")
    async def claim_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        """
        A coroutine that claims the ticket and updates the database.

        Args:
        button (nextcord.ui.Button): The claim button.
        i (nextcord.Interaction): The interaction object.
        """
        try:
            staff_role = nextcord.utils.get(i.guild.roles,id=self.db.staffRole())
            if staff_role not in i.user.roles: return await i.response.send_message("You are not a staff member", ephemeral=True)
            user_id = self.db.execute(sql="SELECT `user-id` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0]
            user = nextcord.utils.get(i.guild.members, id=user_id)
            if user is None: return await i.response.send_message("The user is not in the server anymore", ephemeral=True)
            support_role = self.db.staffRole()
            self.db.execute(sql="UPDATE `Open Tickets` SET `claimed-by` = (?) WHERE `channel_id` = (?)", values=(i.user.id, i.channel.id), fetch=False, commit=True)
            await i.channel.edit(topic=f"Claimed by {i.user.name}")
        except Exception as e:
            if debug: raise e
            else:
                return await i.response.send_message(f"An error occured, please contact the owner.")
            await i.response.send_message(f"{i.user.mention} has claimed this ticket!", ephemeral=False)
        except Exception as e:
            if debug: raise e
            else:
                await i.response.send_message(f"An error occured, please contact the owner.")
    @nextcord.ui.button(label="Close", style=nextcord.ButtonStyle.red, custom_id="close_ticket", emoji="🔒")
    async def close_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
        """
        Closes a ticket and prompts the user for a reason. If no reason is provided, the ticket will be closed without a reason.
        If the user is not a staff member, the function will return a message saying so.
        If the user who opened the ticket is no longer in the server, the function will return a message saying so.
        If transcripts are enabled, the function will create a transcript channel for the ticket type and save the transcript there.
        """
        a = await i.response.defer(with_message="Closing ticket...")
        try:
            staff_role = nextcord.utils.get(i.guild.roles, id=self.db.staffRole())
            if staff_role not in i.user.roles:
                return await i.response.send_message("You are not a staff member", ephemeral=True)

            # Prompt user for reason
            reason_msg = await i.followup.send("Please enter a reason for closing this ticket. You have `60` Seconds.")
            try:
                reason = await self.bot.wait_for("message", check=lambda m: m.author == i.user and m.channel == i.channel, timeout=60.0)
                reason = reason.content
            except asyncio.TimeoutError:
                await reason_msg.delete()
                reason = "No reason provided."
                await i.followup.send("No reason provided. Ticket will be closed without a reason.", ephemeral=True)
            else:
                reason = reason.content

            try:
                user_id = self.db.execute(sql="SELECT `user-id` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0]
                user = nextcord.utils.get(i.guild.members, id=user_id)
                if user is None:
                    return await i.response.send_message("The user is not in the server anymore", ephemeral=True)
            except Exception as e:
                if debug: raise e
                else:
                    await i.response.send_message(f"An error occured, please contact the owner.")
            closed_embed = nextcord.Embed(
                title="Ticket Closed!",
                description=f"This ticket has been closed by {i.user.mention}",
                color=nextcord.Color.red(),
                timestamp=i.message.created_at
            )

            closed_embed.set_footer(text="CCRP | Ticket System")
            closed_embed.add_field(name="📝 Reason", value=reason, inline=False)
            closed_embed.add_field(name="👤 Closed by", value=i.user.mention, inline=False)
            closed_embed.add_field(name="🔓 Opened by", value=user.mention, inline=False)
            closed_embed.add_field(name="⌨️ Ticket type", value=self.db.execute(sql="SELECT `ticket-type` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0], inline=False)

            if self.db.execute(sql="SELECT `claimed-by` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0] != "0":
                try:
                    closed_embed.add_field(name="🛄 Claimed by", value=nextcord.utils.get(i.guild.members, id=self.db.execute(sql="SELECT `claimed-by` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0]).mention, inline=False)
                except Exception as e:
                    closed_embed.add_field(name="🛄 Claimed by", value="No one", inline=False)
            else:
                closed_embed.add_field(name="🛄 Claimed by", value="No one", inline=False)

            if self.db.execute(sql="SELECT `transcripts` FROM `Ticket System`;", fetch=True)[0][0] == 1:
                ticket_type = self.db.execute(sql="SELECT `ticket-type` FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=True)[0][0]
                if ticket_type == "general-support":
                    category = nextcord.utils.get(i.guild.categories, id=int(self.db.execute(sql="SELECT support_category FROM `Ticket System`;", fetch=True)[0][0]))
                    ticket_type_transcripts = nextcord.utils.get(i.guild.channels, name=f"{ticket_type}-transcripts", category=category)
                    if not ticket_type_transcripts:
                        overwrites = {
                            i.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                            staff_role: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                        }
                        ticket_type_transcripts = await category.create_text_channel(f"{ticket_type}-transcripts", overwrites=overwrites)

                elif ticket_type == "donation":
                    category = nextcord.utils.get(i.guild.categories, id=int(self.db.execute(sql="SELECT donation_category FROM `Ticket System`;", fetch=True)[0][0]))
                    ticket_type_transcripts = nextcord.utils.get(i.guild.channels, name=f"{ticket_type}-transcripts", category=category)
                    if not ticket_type_transcripts:
                        overwrites = {
                            i.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                            staff_role: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                        }
                        ticket_type_transcripts = await category.create_text_channel(f"{ticket_type}-transcripts", overwrites=overwrites)
                        
                    elif ticket_type == "ban-appeal":
                        category = nextcord.utils.get(i.guild.categories, id=int(self.db.execute(sql="SELECT ban_category FROM `Ticket System`;", fetch=True)[0][0]))
                        ticket_type_transcripts = nextcord.utils.get(i.guild.channels, name=f"{ticket_type}-transcripts", category=category)
                        if not ticket_type_transcripts:
                            overwrites = {
                                i.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                                staff_role: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                            }
                            ticket_type_transcripts = await category.create_text_channel(f"{ticket_type}-transcripts", overwrites=overwrites)

                        category = self.db.execute(sql="SELECT ban_category FROM `Ticket System`;", fetch=True)[0][0]
                    from utils.generate_transcript import Transcript
                    t = Transcript(self.db)
                    url = await t.generate_transcript(i, i.channel)
                    transcript_file = await user.send(file=nextcord.File(f"transcripts/{i.guild.id}/{i.channel.id}.html"))
                    # url = await t.generate_transcript(i, i.channel, lnk=transcript_file.attachments[0].url)
                    lnk = transcript_file.attachments[0].url
                    transcripturl = lnk.replace("https://cdn.discordapp.com/", "")
                    
                    url = url + transcripturl
                    closed_embed.add_field(name="📜 Direct Transcript", value=f"[Click Me]({url})", inline=False)
                closed_embed.add_field(name="📅 Date", value=i.message.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
                await user.send(embed=closed_embed)
                await ticket_type_transcripts.send(embed=closed_embed)
                await i.channel.delete(reason=reason)

                self.db.execute(sql="DELETE FROM `Open Tickets` WHERE `channel_id` = (?)", values=(i.channel.id,), fetch=False, commit=True)
        except Exception as e:
                if debug:
                    raise e
                else:
                    await i.followup.send(f"An error occured, please contact the owner.")

class OpenTicketDropDown(nextcord.ui.View): # Open a ticket here.
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot
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
        try:
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
                self.db.execute(sql="INSERT INTO `Open Tickets` (uuid, `user-id`, `ticket-type`, channel_id, `is-locked`) VALUES (?, ?, ?, ?, ?)", values=(self.db.randID(), interaction.user.id, "general-support", gen_channel.id, 0), fetch=False, commit=True)
                embed = nextcord.Embed(
                    title="Ticket Opened!",
                    description=general_support_welcome_message.format(member=interaction.user),
                    color=nextcord.Color.green()
                )
                embed.set_footer(text="CCRP | Ticket System")
                await gen_channel.send(content=f"{interaction.user.mention}", delete_after=1)
                await gen_channel.send(embed=embed, view=TicketControlButtons(bot=self.bot))
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
                self.db.execute(sql="INSERT INTO `Open Tickets` (uuid, `user-id`, `ticket-type`, channel_id, `is-locked`) VALUES (?, ?, ?, ?, ?)", values=(self.db.randID(), interaction.user.id, "donation", don_channel.id, 0), fetch=False, commit=True)
                embed = nextcord.Embed(
                    title="Ticket Opened!",
                    description=donation_welcome_message.format(member=interaction.user),
                )
                embed.set_footer(text="CCRP | Ticket System")
                await don_channel.send(embed=embed, view=TicketControlButtons(self.bot))
                await interaction.response.send_message(f"Your ticket has been opened in {don_channel.mention}", ephemeral=True)

            elif select.values[0] == "ban":
                ban_category = nextcord.utils.get(interaction.guild.categories, id=int(self.db.execute(sql="SELECT ban_category FROM `Ticket System`;", fetch=True)[0][0]))
                if ban_category is None: return await interaction.response.send_message("The ban appeal category is not set. Please set it", ephemeral=True)
                support_role = nextcord.utils.get(interaction.guild.roles, id=int(self.db.execute(sql="SELECT support_role FROM `Ticket System`;", fetch=True)[0][0]))
                if support_role is None: return await interaction.response.send_message("The support role is not set. Please set it", ephemeral=True)
                ban_appeal_welcome_message = self.db.execute(sql="SELECT ban_welcome_message FROM `Ticket System`;", fetch=True)[0][0]
                permissions = {
                    interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                    interaction.guild.me: nextcord.PermissionOverwrite(read_messages=True),
                    support_role: nextcord.PermissionOverwrite(read_messages=True),
                    interaction.user: nextcord.PermissionOverwrite(read_messages=True),

                }
                ban_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}", category=ban_category, overwrites=permissions)
                self.db.execute(sql="INSERT INTO `Open Tickets` (uuid, `user-id`, `ticket-type`, channel_id, `is-locked`) VALUES (?, ?, ?, ?, ?)", values=(self.db.randID(), interaction.user.id, "ban-appeal", ban_channel.id, 0), fetch=False, commit=True)
                embed = nextcord.Embed(
                    title="Ticket Opened!",
                    description=ban_appeal_welcome_message.format(member=interaction.user),
                )
                embed.set_footer(text="CCRP | Ticket System")
                await ban_channel.send(embed=embed, view=TicketControlButtons(self.bot))
                await interaction.response.send_message(f"Your ticket has been opened in {ban_channel.mention}", ephemeral=True)
        except Exception as err:
            raise err
            await interaction.response.send_message(f"Error: `{err}`")
class OpenTicketOpenButton(nextcord.ui.View): # Open discord ticket button
        def __init__(self, bot: commands.Bot):
            super().__init__(timeout=None)
            self.bot = bot
            self.db = Database()

        @nextcord.ui.button(label="Open a ticket!", style=nextcord.ButtonStyle.green, custom_id="open_ticket", emoji="🎟️")
        async def open_ticket(self, button: nextcord.ui.Button, i: nextcord.Interaction):
            await i.response.send_message("In order to open a ticket, please select a category", ephemeral=True, view=OpenTicketDropDown(self.bot))

        
    


class StartTicketSystem(commands.Cog): # Start Ticket System
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.db = Database()

    @nextcord.slash_command(name="start-ticket-system", description="Start the ticket system", force_global=True)
    @application_checks.has_guild_permissions(manage_guild=True)
    async def _start_ticket_system(self, i: nextcord.Interaction):
        ticket_channel = nextcord.utils.get(i.guild.channels, id=int(self.db.execute(sql="SELECT ticket_channel FROM `Ticket System`;", fetch=True)[0][0]))
        if ticket_channel is None: return await i.response.send_message("The ticket channel is not set. Please set it", ephemeral=True)
        support_role = nextcord.utils.get(i.guild.roles, id=int(self.db.execute(sql="SELECT support_role FROM `Ticket System`;", fetch=True)[0][0]))
        if support_role is None: return await i.response.send_message("The support role is not set. Please set it", ephemeral=True)
        embed = nextcord.Embed(
            title="Open a ticket!",
            description="React with 🎟️ to open a ticket",
            color=nextcord.Color.green(),
            
        )
        embed.set_footer(text="CCRP | Ticket System")
        await ticket_channel.send(embed=embed, view=OpenTicketOpenButton(self.bot))
        await i.response.send_message("The ticket system has been started!", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(StartTicketSystem(bot))
