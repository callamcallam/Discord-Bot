import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import nextcord


class Transcript:
    def __init__(self, db):
        """
        Initializes a Transcript object.

        Args:
        - db: a database object
        """
        self.db = db
        
    async def generate_transcript(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel) -> str:
        """
        Generates a transcript of a given channel and sends it to the user.

        Args:
        - interaction: a nextcord.Interaction object
        - channel: a nextcord.TextChannel object

        Returns:
        - a string containing the URL of the generated transcript
        """
        try:
            staff_role = nextcord.utils.get(interaction.guild.roles, id=self.db.staffRole())
            if staff_role not in interaction.user.roles:
                return await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)


            path = f'./transcripts/{interaction.guild.id}/'
            async with channel.typing():
                if not os.path.exists(path):
                    os.makedirs(path)

                text_log = await channel.history(limit=None).flatten()
                with open(f"transcripts/{interaction.guild.id}/{channel.id}.html", "w", encoding='utf-8-sig', errors="ignore") as f:
                    f.write('<html>\n')
                    f.write('<head>\n')
                    f.write('<style>\n')
                    f.write('<link rel="icon" type="image/x-icon" href="/images/favicon.ico">')
                    f.write('body { font-family: Arial, sans-serif; background-color: #424549; padding: 20px;}\n')
                    f.write('.transcript { max-width: 800px; margin: 0 auto; background-color: #36393e; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); padding: 20px;}\n')
                    f.write('.message { margin-bottom: 20px; border-left: 4px solid #007bff; padding-left: 10px; display: flex; flex-direction: row; align-items: flex-start; }\n')
                    f.write('.avatar { width: 32px; height: 32px; border-radius: 50%; margin-right: 10px; }\n')
                    f.write('.author { font-weight: bold; color: #007bff; margin-bottom: 5px;}\n')
                    f.write('.content { color: #FFF; }\n')
                    f.write('.timestamp { color: #999; font-size: 14px; margin-left: auto; }\n')
                    f.write('.transcript label { color: #FFF; font-size: 25px; }\n')  # Change the color to white
                    f.write('</style>\n')
                    f.write('</head>\n')
                    f.write('<body>\n')
                    f.write('<title>Central City RP | Transcripts</title>\n')
                    f.write('<div class="transcript">')
                    f.write(f'<label><b>{interaction.guild.name} | {channel.name}</b><br><br></label>')

                    for message in text_log:
                        current_time = datetime.now()
                        message_time = message.created_at

                        if current_time.date() == message_time.date():
                            timestamp = "Today at: " + message_time.strftime("%H:%M:%S")
                        elif current_time.date() - message_time.date() == relativedelta(days=1):
                            timestamp = "Yesterday at: " + message_time.strftime("%H:%M:%S")
                        else:
                            timestamp = message_time.strftime("%A, %B %d, %Y at %H:%M:%S")

                        f.write('<div class="message">\n')
                        f.write(f'<img src="{message.author.avatar.url}" alt="Avatar" class="avatar">\n')
                        f.write('<div class="message-content">\n')
                        f.write(f'<span class="author">{message.author.display_name}:</span>\n')
                        f.write(f'<span class="content">{message.content}</span>\n')
                        f.write('</div>\n')
                        f.write(f'<span class="timestamp">{timestamp}</span>\n')
                        f.write('</div>\n')

                    f.write('</div>')
                    f.write('</body>\n')
                    f.write('</html>\n')


    
            return f"https://transcripts.centralcityrp.uk/transcripts/"
        except Exception as e:
            return "Error generating transcript! Error: " + str(e)
