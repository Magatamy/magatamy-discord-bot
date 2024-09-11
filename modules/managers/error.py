from disnake import MessageInteraction, ModalInteraction
from config import ERROR_LOG_CHANNEL, LANGUAGES_DEFAULT

from ..enums import ErrorType
from .language import LanguageManager
from ..generators import EmbedGenerator


class ErrorManager:
    @staticmethod
    async def error_handle(inter: MessageInteraction | ModalInteraction, type_error: ErrorType, action=None):
        language = LanguageManager(locale=inter.locale)
        log_language = LanguageManager(locale=LANGUAGES_DEFAULT)
        log_channel = inter.client.get_channel(ERROR_LOG_CHANNEL)

        if type_error == ErrorType.BUTTON_TIMEOUT.value:
            log_response = log_language.get_embed_data('button_timeout_log_error')
            response = language.get_embed_data('button_timeout_error')
        elif type_error == ErrorType.MODAL_TIMEOUT.value:
            log_response = log_language.get_embed_data('modal_timeout_log_error')
            response = language.get_embed_data('modal_timeout_error')
        else:
            log_response = log_language.get_embed_data('unknown_timeout_log_error')
            response = language.get_embed_data('unknown_timeout_error')

        await inter.author.send(embed=EmbedGenerator(json_schema=response))
        await log_channel.send(embed=EmbedGenerator(json_schema=log_response, action=action))
