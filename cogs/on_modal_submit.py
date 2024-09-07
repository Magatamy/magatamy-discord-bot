from disnake import ModalInteraction
from disnake.ext import commands

from modules.database import GuildSettingsTable
from modules.generators import EmbedGenerator
from modules.managers import LanguageManager
from modules.enums import ModalID, ModalInputID


class OnModalSubmit(commands.Cog):
    @commands.Cog.listener()
    async def on_modal_submit(self, inter: ModalInteraction):
        settings = GuildSettingsTable(guild_id=inter.guild.id)
        await settings.load()
        language = LanguageManager(locale=inter.locale, language=settings.language)
        modal_actions = {
            ModalID.CHANGE_NAME.value: self.change_name,
            ModalID.CHANGE_LIMIT.value: self.change_limit
        }
        action = modal_actions.get(inter.custom_id)
        if action:
            await action(inter, language)

    @staticmethod
    async def change_name(inter: ModalInteraction, language: LanguageManager):
        new_name = inter.text_values.get(ModalInputID.CHANGE_NAME.value)
        await inter.author.voice.channel.edit(name=new_name)

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

        await inter.response.send_message(embed=EmbedGenerator(json_schema=response, limit=new_limit), ephemeral=True)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnModalSubmit(client))
