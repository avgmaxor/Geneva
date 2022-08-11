from distutils.cmd import Command
import discord
from pathlib import Path
from discord_webhook import DiscordWebhook

currentdir = str(Path().absolute())

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as host: ',self.user)
        sending233 = DiscordWebhook(url='https://discord.com/api/webhooks/1006756471872163940/O4DjO3ADxjT3Orfw645bTuCfhV6mIBn4i7SfX77mUayVNTqLLOVPLpAKcMZrLrR2r6hx', content='Client 2 has connected')
        sent233 = sending233.execute()     

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        await message.channel.send('updating player data')
        with open(currentdir + '/multiplayer/server/maxor1.txt', 'w') as f:
            f.write(message.content)

client = MyClient()
client.run('ODQzNTE3MzM1MTM0NjY2NzYy.GlIV97.H1MTzxulJ0eaebBEx7JLS2i2SrRGShCRe7iKKw')