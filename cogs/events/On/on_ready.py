import nextcord, datetime, os
from nextcord.ext import commands
from utils.sqlitedatabase import Database
from utils.webhook import Webhook
# from cogs.commands.tickets import TicketSystemCloseButton, TicketSystemButtons, TicketSystemLockConfirmationButtons, TicketSystemDropDown, TicketSystemCloseConfirmation


class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = Database()
        self.webhook = Webhook(url=self.db.execute(sql="SELECT webhook_url FROM Config;", fetch=True)[0][0])

    async def change_status(self):
        await self.bot.wait_until_ready()
        # views = [TicketSystemButtons(), TicketSystemLockConfirmationButtons(), TicketSystemCloseButton(), TicketSystemDropDown(), TicketSystemCloseConfirmation()]
        # for view in views: self.bot.add_view(view)
        activity_type = self.db.execute(sql="SELECT status_type FROM Config;", fetch=True)[0][0]
        status = self.db.execute(sql="SELECT status FROM Config;", fetch=True)[0][0]

        if activity_type == "playing":
            activity = nextcord.Game(name=status)
        elif activity_type == "listening":
            activity = nextcord.Activity(type=nextcord.ActivityType.listening, name=status)
        elif activity_type == "watching":
            activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=status)
        elif activity_type == "competing":
            activity = nextcord.Activity(type=nextcord.ActivityType.competing, name=status)

        await self.bot.change_presence(activity=activity)
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await self.change_status()
        # commands = [command[:-3] for command in os.listdir("cogs/commands/fivem") if command.endswith(".py")]
        # await self.bot.sync_application_commands(data=commands,guild_id=1092591199300370473)
        # commands = [command for command in os.listdir("cogs/commands") if command.endswith(".py")]
        # events = [event for event in os.listdir("cogs/events") if event.endswith(".py")]

        print(f"{self.bot.user.name} is ready!")
        print(f"Bot ID: {self.bot.user.id}")
        print(f"Bot prefix: {self.db.execute(sql='SELECT command_prefix FROM Config;', fetch=True)[0][0]}")
        print(f"Bot status: {self.db.execute(sql='SELECT status FROM Config;', fetch=True)[0][0]}")
        print(f"Bot status type: {self.db.execute(sql='SELECT status_type FROM Config;', fetch=True)[0][0]}")
        embed = nextcord.Embed(
            title=f"{str(self.bot.user.name)} | Bot Started",
            description=f"""
- 👤 Bot Username: **{self.bot.user.name}**
- 🆔 Bot ID: **{self.bot.user.id}**
- 📜 Bot Prefix: **{self.db.execute(sql='SELECT command_prefix FROM Config;', fetch=True)[0][0]}**
- 🟢 Bot Status: **{self.db.execute(sql='SELECT status FROM Config;', fetch=True)[0][0]}**
- 🎮 Bot Status Type: **{self.db.execute(sql='SELECT status_type FROM Config;', fetch=True)[0][0]}**
- 📶 Bot API Latency: **{self.bot.latency}**
            """,
            color=nextcord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        # for command in commands: embed.add_field(name="Command Loaded", value=f"`{command[:-3]}`")
        # for event in events: embed.add_field(name="Event Loaded", value=f"`{event[:-3]}`")

        self.webhook.send(content=embed.to_dict(), embed=True)


def setup(bot: commands.Bot):
    bot.add_cog(OnReady(bot))