import os
import requests
from pprint import pprint


url = f"https://discord.com/api/v10/applications/{os.getenv('DISCORD_APP_ID')}/commands"

# For authorization, you can use either your bot token
headers = {"Authorization": f"Bot {os.getenv("DISCORD_TOKEN")}"}

r = requests.get(url, headers=headers)
pprint(r.json())
