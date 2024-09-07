from disnake.ext import commands, tasks
from datetime import datetime, timedelta
from pytz import FixedOffset

from modules.database import SaturdayChannelsTable, GuildSettingsTable
from modules.managers import LanguageManager
from modules.generators import EmbedGenerator


class Loops(commands.Cog):
    def __init__(self, client: commands.AutoShardedInteractionBot):
        self.client = client
        self.start_saturday.start()

    @tasks.loop(minutes=1)
    async def start_saturday(self):
        saturdays = SaturdayChannelsTable()
        await saturdays.load_all()
        for saturday in saturdays:
            channel = self.client.get_channel(saturday.channel_id)
            if not channel:
                await saturday.delete_data()
                continue

            settings = GuildSettingsTable(guild_id=channel.guild.id)
            await settings.load()
            language = LanguageManager(locale=channel.guild.preferred_locale, language=settings.language)

            offset_hours = int(saturday.timezone.replace('UTC', ''))
            timezone = FixedOffset(offset_hours * 60)
            today = datetime.now(timezone)
            time_to_subtract = timedelta(hours=saturday.time.hour, minutes=saturday.time.minute)
            need_time = today - time_to_subtract

            if need_time.weekday() == 5 and not saturday.started_saturday:
                saturday.started_saturday = True
                overwrite = channel.overwrites_for(channel.guild.default_role)
                overwrite.send_messages = None
                message = language.get_embed_data(json_key='message_start_saturday')
            elif need_time.weekday() != 5 and saturday.started_saturday:
                saturday.started_saturday = False
                overwrite = channel.overwrites_for(channel.guild.default_role)
                overwrite.send_messages = False
                message = language.get_embed_data(json_key='message_end_saturday')
            else:
                continue

            await saturday.update()
            await channel.set_permissions(target=channel.guild.default_role, overwrite=overwrite)
            await channel.send(embed=EmbedGenerator(json_schema=message))

    @start_saturday.before_loop
    async def before_start_saturday(self):
        await self.client.wait_until_ready()


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(Loops(client))
