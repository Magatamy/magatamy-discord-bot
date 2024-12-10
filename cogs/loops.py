import time

from disnake.ext import commands, tasks
from modules.redis import Subscriptions


class Loops(commands.Cog):
    def __init__(self, client: commands.AutoShardedInteractionBot):
        self.client = client
        self.check_subscription.start()

    @tasks.loop(minutes=1)
    async def check_subscription(self):
        guilds = self.client.guilds
        for guild in guilds:
            guild_sub = Subscriptions(key=guild.id)

            if await guild_sub.load():
                if guild_sub.is_forever:
                    continue

                now_ts = int(time.time() * 1000)

                if guild_sub.timestamp:
                    if now_ts < guild_sub.timestamp:
                        continue

            await guild.leave()

    @check_subscription.before_loop
    async def before_check_subscription(self):
        await self.client.wait_until_ready()


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(Loops(client))
