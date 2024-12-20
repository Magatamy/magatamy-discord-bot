import time
import aiohttp

from disnake.ext import commands, tasks
from modules.redis import Subscriptions
from config import WEB_API_DOMAIN, WEB_API_SECRET_KEY


class Loops(commands.Cog):
    def __init__(self, client: commands.AutoShardedInteractionBot):
        self.client = client
        self.check_subscription.start()
        self.push_bot_data.start()

    @tasks.loop(minutes=1)
    async def check_subscription(self):
        guilds = self.client.guilds
        for guild in guilds:
            guild_sub = Subscriptions(key=guild.id)

            if await guild_sub.load():
                if guild_sub.is_forever:
                    continue

                now_ts = int(time.time() * 1000)

                if guild_sub.expiry_ts and now_ts < guild_sub.expiry_ts:
                    continue

            await guild.leave()

    @tasks.loop(minutes=5)
    async def push_bot_data(self):
        servers = 0
        users = 0
        channels = 0
        top_servers = []
        for guild in self.client.guilds:
            guild_users = len(guild.members)

            servers += 1
            users += guild_users
            channels += len(guild.channels)
            top_servers.append({
                "name": guild.name,
                "icon_url": guild.icon.url,
                "users": guild_users
            })

        top_servers.sort(key=lambda x: x["users"], reverse=True)

        headers = {"x-secret-key": WEB_API_SECRET_KEY}
        payload = {
            "bot_id": self.client.user.id,
            "servers": servers,
            "users": users,
            "channels": channels,
            "weekly_users": [1, 2, 3, 4, 5, 6, 7],
            "weekly_servers": [1, 2, 3, 4, 5, 6, 7],
            "top_servers": top_servers[:10]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{WEB_API_DOMAIN}/discord/botData", json=payload, headers=headers):
                pass

    @check_subscription.before_loop
    async def before_check_subscription(self):
        await self.client.wait_until_ready()

    @push_bot_data.before_loop
    async def before_push_bot_data(self):
        await self.client.wait_until_ready()


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(Loops(client))
