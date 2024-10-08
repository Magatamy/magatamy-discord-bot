from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from modules.managers import Localized, LanguageManager, LANGUAGES_DATA
from modules.redis import GuildSettings
from modules.generators import EmbedGenerator

LANGUAGES_CHOICES = ['disable', *list(LANGUAGES_DATA.keys())]
COMMAND_NAME = Localized('language_name')
COMMAND_DESCRIPTION = Localized('language_description')
LANGUAGES_DESCRIPTION = Localized('language_param_description')


class Language(commands.Cog):
    @commands.slash_command(name=COMMAND_NAME, description=COMMAND_DESCRIPTION)
    @commands.cooldown(rate=2, per=10)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def language(
            self, inter: ApplicationCommandInteraction,
            language: str = commands.Param(
                default='disable', choices=LANGUAGES_CHOICES, description=LANGUAGES_DESCRIPTION)):
        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        if language == 'disable':
            settings.language = None
            json_key = 'disable_language'
        else:
            settings.language = language
            json_key = 'change_language'
        await settings.save()

        language = LanguageManager(locale=inter.locale, language=settings.language)
        response = language.get_embed_data(json_key)
        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(Language(client))
