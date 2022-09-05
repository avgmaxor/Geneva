import discord
from pathlib import Path
from discord_webhook import DiscordWebhook
# PREVENT CRASHES
currentdir = str(Path().absolute())

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as p2: ',self.user)
        sending233 = DiscordWebhook(url='https://discord.com/api/webhooks/1006739051082166373/0C-x9_DMsqD8-5KtdtQIheDmVQUtsrU2Ml4ktNh5vpoYKfHZdSI4_JowVUrqhinTgsrd', content='Client 2 has connected')
        sent233 = sending233.execute()     

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        await message.channel.send('updating player data')
        with open(currentdir + '/multiplayer/server/maxor2.txt', 'w') as f:
            f.write(message.content)

client = MyClient()
# Token Removed [and changed]
client.run('')