import discord
from pathlib import Path

currentdir = str(Path().absolute())

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        await message.channel.send('updating player data')
        with open(currentdir + '/server/maxor.txt', 'w') as f:
            f.write(message.content)

client = MyClient()
client.run('MTAwNjc0MDgyMTUzMTQzNTAwOA.G6J2M7.sGDlQMkBlYbAWy2twG_J4fJarqNd6EIBt7cne4')