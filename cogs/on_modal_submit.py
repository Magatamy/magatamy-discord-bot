from disnake import ModalInteraction
from disnake.ext import commands

from modules.redis import GuildSettings
from modules.managers import LanguageManager
from utils.modal_hendlers.modal_mapping import get_modal_actions


class OnModalSubmit(commands.Cog):
    @commands.Cog.listener()
    async def on_modal_submit(self, inter: ModalInteraction):
        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        language = LanguageManager(locale=inter.locale, language=settings.language)
        action = get_modal_actions().get(inter.custom_id)
        if action:
            await action(inter, language)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnModalSubmit(client))
