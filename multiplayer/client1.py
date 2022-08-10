from distutils.cmd import Command
import discord
from pathlib import Path

currentdir = str(Path().absolute())

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as host: ',self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        await message.channel.send('updating player data')
        with open(currentdir + 'multiplayer/server/maxor.txt', 'w') as f:
            f.write(message.content)

client = MyClient()
client.run('ODQzNTE3MzM1MTM0NjY2NzYy.GlIV97.H1MTzxulJ0eaebBEx7JLS2i2SrRGShCRe7iKKw')