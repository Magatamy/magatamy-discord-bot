from config import magatamy_guilds
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from modules.managers import LanguageManager, Localized, ButtonManager
from modules.generators import EmbedGenerator
from modules.enums import ButtonID
from modules.redis import GuildSettings

COMMAND_NAME = Localized('create_request_vanilla_name')
COMMAND_DESCRIPTION = Localized('create_request_vanilla_description')


class CreateRequestVanilla(commands.Cog):
    @commands.slash_command(name=COMMAND_NAME, description=COMMAND_DESCRIPTION, guild_ids=magatamy_guilds)
    @commands.cooldown(rate=2, per=10)
    @commands.has_permissions(administrator=True)
    async def create_request_vanilla(self, inter: ApplicationCommandInteraction):
        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        language = LanguageManager(locale=inter.locale, language=settings.language)

        post_text, response = language.get_embed_data(['create_request_vanilla', 'create_request_vanilla_response'])
        button_label = language.get_static('button_request_vanilla')

        buttons = ButtonManager()
        buttons.add_button(custom_id=ButtonID.POST_REQUEST_VANILLA.value, label=button_label)

        await inter.channel.send(embed=EmbedGenerator(json_schema=post_text), components=buttons.components)
        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)


def setup(client):
    client.add_cog(CreateRequestVanilla(client))
