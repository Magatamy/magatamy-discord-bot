from disnake import ModalInteraction
from disnake.ext import commands
from asyncio import wait_for, TimeoutError

from modules.redis import GuildSettings, Users
from modules.generators import EmbedGenerator
from modules.managers import LanguageManager, ErrorManager
from modules.enums import ModalID, ModalInputID, ErrorType


class OnModalSubmit(commands.Cog):
    @commands.Cog.listener()
    async def on_modal_submit(self, inter: ModalInteraction):
        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        language = LanguageManager(locale=inter.locale, language=settings.language)
        modal_actions = {
            ModalID.CHANGE_NAME.value: self.change_name,
            ModalID.CHANGE_LIMIT.value: self.change_limit
        }
        action = modal_actions.get(inter.custom_id)
        try:
            if action:
                await wait_for(action(inter, language), timeout=5)
        except TimeoutError:
            await ErrorManager.error_handle(inter=inter, type_error=ErrorType.MODAL_TIMEOUT.value, action=action)

    @staticmethod
    async def change_name(inter: ModalInteraction, language: LanguageManager):
        new_name = inter.text_values.get(ModalInputID.CHANGE_NAME.value)
        await inter.author.voice.channel.edit(name=new_name)

        user = Users(key=inter.author.id)
        user.private_name = new_name
        await user.save()

        response = language.get_embed_data('change_name_response')
        await inter.response.send_message(embed=EmbedGenerator(json_schema=response, name=new_name), ephemeral=True)

    @staticmethod
    async def change_limit(inter: ModalInteraction, language: LanguageManager):
        new_limit = inter.text_values.get(ModalInputID.CHANGE_LIMIT.value)

        if not new_limit.isdigit() or not (0 <= int(new_limit) <= 99):
            response = language.get_embed_data('error_change_limit_value')
        else:
            await inter.author.voice.channel.edit(user_limit=new_limit)
            response = language.get_embed_data('change_limit_response')

            user = Users(key=inter.author.id)
            user.private_limit = new_limit
            await user.save()

        await inter.response.send_message(embed=EmbedGenerator(json_schema=response, limit=new_limit), ephemeral=True)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnModalSubmit(client))
