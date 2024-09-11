from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from config import ERROR_LOG_CHANNEL, LANGUAGES_DEFAULT

from modules.managers import LanguageManager
from modules.generators import EmbedGenerator


class OnSlashCommandError(commands.Cog):
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: ApplicationCommandInteraction, error: commands.CommandError):
        language = LanguageManager(locale=inter.locale)
        log_language = LanguageManager(locale=LANGUAGES_DEFAULT)

        if isinstance(error, commands.CommandOnCooldown):
            data = int(error.retry_after)
            response = language.get_embed_data('command_on_cooldown')
        else:
            response = language.get_embed_data('unknown_error')
            log_response = log_language.get_embed_data('unknown_log_error')

            log_channel = inter.client.get_channel(ERROR_LOG_CHANNEL)
            await log_channel.send(embed=EmbedGenerator(json_schema=log_response, error=error))
            await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)

            raise error

        await inter.response.send_message(embed=EmbedGenerator(json_schema=response, data=data), ephemeral=True)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnSlashCommandError(client))
