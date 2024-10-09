from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from modules.managers import Localized, LanguageManager
from modules.generators import EmbedGenerator
from modules.redis import GuildSettings
from config import OWNER_IDS

COMMAND_NAME = Localized('help_name')
COMMAND_DESCRIPTION = Localized('help_description')


class Help(commands.Cog):
    def __init__(self, client: commands.AutoShardedInteractionBot):
        self.client = client

    @commands.slash_command(name=COMMAND_NAME, description=COMMAND_DESCRIPTION)
    @commands.cooldown(rate=2, per=10)
    @commands.guild_only()
    async def help(self, inter: ApplicationCommandInteraction):
        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        language = LanguageManager(locale=inter.locale, language=settings.language)

        response = language.get_embed_data('help_response')
        command_help, command_help_description = language.get_slash_commands(['help_name', 'help_description'])

        user = ', '.join([self.client.get_user(user_id).name for user_id in OWNER_IDS])

        await inter.response.send_message(embed=EmbedGenerator(
            json_schema=response,
            lenght_guilds=len(self.client.guilds),
            image_client=self.client.user.avatar,
            owners=user,
            command_help=command_help,
            command_help_description=command_help_description
        ), ephemeral=True)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(Help(client))

