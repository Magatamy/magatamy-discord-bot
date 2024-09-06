from config import custom_magatamy_guilds
from disnake import ApplicationCommandInteraction, Member
from disnake.ext import commands

from modules.database import RequestVanilla
from modules.managers import LanguageManager, Localized
from modules.generators import EmbedGenerator

COMMAND_NAME = Localized('remove_request_vanilla_name')
COMMAND_DESCRIPTION = Localized('remove_request_vanilla_description')


class RemoveRequestVanilla(commands.Cog):
    @commands.slash_command(name=COMMAND_NAME, description=COMMAND_DESCRIPTION, guild_ids=custom_magatamy_guilds)
    @commands.has_permissions(administrator=True)
    async def remove_request_vanilla(self, inter: ApplicationCommandInteraction, user: Member):
        language = LanguageManager(locale=inter.locale)
        request = RequestVanilla(member_id=user.id)
        if await request.delete():
            response = language.get_embed_data('remove_request_vanilla')
        else:
            response = language.get_embed_data('remove_request_vanilla_error')

        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)


def setup(client):
    client.add_cog(RemoveRequestVanilla(client))
