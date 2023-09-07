import nextcord, requests
from nextcord.ext import commands


import requests
import json

class Webhook:
    def __init__(self, url: str):
        self.url = url

    def send(self, content: str, embed: bool = False):
        headers = {'Content-Type': 'application/json'}
        if embed:
            data = {"embeds": [content]}
        else:
            data = {"content": content}
        response = requests.post(self.url, data=json.dumps(data), headers=headers)


    