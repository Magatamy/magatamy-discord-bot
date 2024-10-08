from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from modules.managers import Localized, LanguageManager
from modules.generators import EmbedGenerator
from modules.redis import GuildSettings
from modules.enums import ButtonID, Emoji
from utils.buttons.message_settings_components import get_components
from config import OWNER_IDS

COMMAND_NAME = Localized('help_name')
COMMAND_DESCRIPTION = Localized('help_description')

class Information(commands.Cog):
    def __init__(self, client: commands.AutoShardedInteractionBot):
        self.client = client

    @commands.slash_command(name=COMMAND_NAME, description=COMMAND_DESCRIPTION)
    @commands.cooldown(rate=2, per=10)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def create_private_channel(self, inter: ApplicationCommandInteraction):
        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        language = LanguageManager(locale=inter.locale, language=settings.language)

        response = language.get_embed_data('help')
        command_help = language.get_slash_commands('help_name')
        command_help_description = language.get_slash_commands('help_description')
        user = ''
        for id in OWNER_IDS:
            user += f'{self.client.get_user(id).name} (**{self.client.get_user(id).display_name}**)'
        await inter.response.send_message(embed=EmbedGenerator(
            json_schema=response,
            lenght_guilds=len(self.client.guilds),
            image_client=self.client.user.avatar,
            owners=user,
            command_help=command_help,
            command_help_description=command_help_description), ephemeral=True)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(Information(client))

