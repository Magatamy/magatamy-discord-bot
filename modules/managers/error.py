from disnake import MessageInteraction, ModalInteraction
from config import ERROR_LOG_CHANNEL, LANGUAGES_DEFAULT
from asyncio import TimeoutError

from modules.managers import LanguageManager
from modules.generators import EmbedGenerator


class ErrorManager:
    @staticmethod
    async def error_handle(inter: ModalInteraction, error: Exception):
        language = LanguageManager(locale=inter.locale)
        log_language = LanguageManager(locale=LANGUAGES_DEFAULT)

        if isinstance(error, TimeoutError):
            response = language.get_embed_data('edit_name_timeout')
            await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)
        else:
            log_channel = inter.client.get_channel(ERROR_LOG_CHANNEL)
            log_response = log_language.get_embed_data('unknown_log_error')
            response = language.get_embed_data('unknown_error')

            await inter.author.send(embed=EmbedGenerator(json_schema=response))
            await log_channel.send(embed=EmbedGenerator(json_schema=log_response, action=error))
