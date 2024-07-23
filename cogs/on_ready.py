from disnake.ext import commands


class OnReady(commands.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is Ready!')


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnReady(client))
