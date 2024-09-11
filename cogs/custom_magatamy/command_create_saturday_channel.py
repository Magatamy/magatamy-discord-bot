from config import magatamy_guilds

from datetime import time
from disnake import ApplicationCommandInteraction, TextChannel
from disnake.ext import commands

from modules.managers import Localized, LanguageManager
from modules.generators import EmbedGenerator
from modules.redis import SaturdayChannels, GuildSettings

COMMAND_NAME = Localized('create_saturday_channel_name')
COMMAND_DESCRIPTION = Localized('create_saturday_channel_description')
COMMAND_PARAM_TIMEZONE_DESCRIPTION = Localized('create_saturday_channel_param_timezone_description')
COMMAND_PARAM_HOUR_DESCRIPTION = Localized('create_saturday_channel_param_hour_description')
COMMAND_PARAM_MINUTE_DESCRIPTION = Localized('create_saturday_channel_param_minute_description')
TIMEZONES = ['UTC+0', 'UTC+1', 'UTC+2', 'UTC+3', 'UTC+4', 'UTC+5', 'UTC+6', 'UTC+7', 'UTC+8',
             'UTC+9', 'UTC+10', 'UTC+11', 'UTC+12', 'UTC-1', 'UTC-2', 'UTC-3', 'UTC-4', 'UTC-5',
             'UTC-6', 'UTC-7', 'UTC-8', 'UTC-9', 'UTC-10', 'UTC-11', 'UTC-12']


class CreateSaturdayChannel(commands.Cog):
    @commands.slash_command(name=COMMAND_NAME, description=COMMAND_DESCRIPTION, guild_ids=magatamy_guilds)
    @commands.cooldown(rate=2, per=10)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def create_saturday_channel(
            self,
            inter: ApplicationCommandInteraction,
            channel: TextChannel,
            timezone: str = commands.Param(choices=TIMEZONES, description=COMMAND_PARAM_TIMEZONE_DESCRIPTION),
            hour: int = commands.Param(
                default=0, min_value=1, max_value=23, description=COMMAND_PARAM_HOUR_DESCRIPTION),
            minute: int = commands.Param(
                default=0, min_value=1, max_value=59, description=COMMAND_PARAM_MINUTE_DESCRIPTION)
    ):
        saturday = SaturdayChannels(key=channel.id)
        await saturday.load()
        saturday.timezone = timezone
        saturday.timestamp = ((hour * 60 * 60) + (minute * 60)) * 1000
        await saturday.save()

        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        language = LanguageManager(locale=inter.locale, language=settings.language)
        response = language.get_embed_data(json_key='create_saturday_channel')
        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(CreateSaturdayChannel(client))
