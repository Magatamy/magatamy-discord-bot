from disnake import MessageInteraction
from disnake.ext import commands

from modules.redis import GuildSettings
from modules.managers import LanguageManager
from utils.button_handlers.button_mapping import get_button_actions


class OnButtonClick(commands.Cog):
    @commands.Cog.listener()
    async def on_button_click(self, inter: MessageInteraction):
        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        language = LanguageManager(locale=inter.locale, language=settings.language)
        action = get_button_actions().get(inter.component.custom_id)
        if action:
            await action(inter, language)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnButtonClick(client))
