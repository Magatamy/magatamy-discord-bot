import time
import aiohttp
import datetime

from disnake.ext import commands, tasks
from modules.redis import Subscriptions, WeeklyData
from config import WEB_API_DOMAIN, WEB_API_SECRET_KEY


class Loops(commands.Cog):
    def __init__(self, client: commands.AutoShardedInteractionBot):
        self.client = client
        self.check_subscription.start()
        self.push_bot_data.start()
        self.update_weekly_data.start()

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

    @tasks.loop(minutes=10)
    async def push_bot_data(self):
        weekly_data = WeeklyData(key=self.client.user.id)
        await weekly_data.load()

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
                "icon_url": guild.icon.url if guild.icon else self.client.user.avatar.url,
                "users": guild_users
            })

        top_servers.sort(key=lambda x: x["users"], reverse=True)

        headers = {"x-secret-key": WEB_API_SECRET_KEY}
        payload = {
            "bot_id": self.client.user.id,
            "servers": servers,
            "users": users,
            "channels": channels,
            "weekly_users": weekly_data.weekly_users,
            "weekly_servers": weekly_data.weekly_servers,
            "top_servers": top_servers[:10]
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(f"{WEB_API_DOMAIN}/discord/botData", json=payload, headers=headers) as response:
                if response.status != 200:
                    print(f"Failed push bot data {response.status}:", await response.text())

    @tasks.loop(minutes=5)
    async def update_weekly_data(self):
        today = datetime.date.today()
        weekday_number = today.weekday()

        users = 0
        servers = 0
        for guild in self.client.guilds:
            servers += 1
            users += len(guild.members)

        data = WeeklyData(key=self.client.user.id)
        await data.load()
        weekly_users = data.weekly_users
        weekly_servers = data.weekly_servers

        if data.weekday_number != weekday_number:
            data.weekday_number = weekday_number
            weekly_users.pop(0)
            weekly_servers.pop(0)
            weekly_users.append(users)
            weekly_servers.append(servers)
        else:
            weekly_users[-1] = users
            weekly_servers[-1] = servers

        data.weekly_users = weekly_users
        data.weekly_servers = weekly_servers
        await data.save()

    @check_subscription.before_loop
    async def before_check_subscription(self):
        await self.client.wait_until_ready()

    @push_bot_data.before_loop
    async def before_push_bot_data(self):
        await self.client.wait_until_ready()

    @update_weekly_data.before_loop
    async def before_update_weekly_data(self):
        await self.client.wait_until_ready()


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(Loops(client))
