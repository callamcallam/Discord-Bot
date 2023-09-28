import nextcord
from utils.sqlitedatabase import Database
from nextcord.ext import commands
db = Database()
bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all(), case_insensitive=False, help_command=None)

@nextcord.slash_command(
    name="xxx",
    description="API Latency",
    # guild_ids=[1092591199300370473]
)
async def ping(i: nextcord.Interaction):
    return await i.response.send_message(f"Pong! {round(bot.latency * 1000)}ms", ephemeral=True)


bot.run(db.execute(sql="SELECT `token` FROM `Config`;",fetch=True)[0][0])