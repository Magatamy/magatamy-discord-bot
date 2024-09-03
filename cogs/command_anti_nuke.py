from disnake import ApplicationCommandInteraction, Role
from disnake.ext import commands

from modules.managers import Localized, LanguageManager
from modules.generators import EmbedGenerator
from modules.database import AntiNukeTable

COMMAND_NAME = Localized('anti_nuke_name')
BLOCK_ROLE_NAME = Localized('anti_nuke_block_role_name')
BLOCK_ROLE_DESCRIPTION = Localized('anti_nuke_block_role_description')

BAN_PROTECTION_NAME = Localized('anti_nuke_ban_protection_description')
BAN_PROTECTION_DESCRIPTION = Localized('anti_nuke_ban_protection_description')


class AntiNuke(commands.Cog):
    def __init__(self, client: commands.AutoShardedInteractionBot):
        self.client = client

    @commands.slash_command(name=COMMAND_NAME)
    @commands.cooldown(rate=2, per=10)
    @commands.has_permissions(administrator=True)
    async def anti_nuke(self, inter: ApplicationCommandInteraction):
        pass

    @anti_nuke.sub_command(name=BLOCK_ROLE_NAME, description=BLOCK_ROLE_DESCRIPTION)
    async def block_role(self, inter: ApplicationCommandInteraction, role: Role):
        language = LanguageManager(locale=inter.guild_locale)
        anti_nuke = AntiNukeTable(guild_id=inter.guild.id)
        await anti_nuke.load()

        if anti_nuke.block_role_id == role.id:
            response = language.get_embed_data(json_key='anti_nuke_block_role_error')
        else:
            response = language.get_embed_data(json_key='anti_nuke_block_role')
            anti_nuke.block_role_id = role.id
            await anti_nuke.update()

        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)
        pass

    @anti_nuke.sub_command(name=BAN_PROTECTION_NAME, description=BAN_PROTECTION_DESCRIPTION)
    async def ban_protection(self, inter: ApplicationCommandInteraction,
                             hour: int = commands.Param(
                                 default=0, min_value=1, max_value=24, description=BAN_PROTECTION_HOUR_DESCRIPTION),
                             minute: int = commands.Param(
                                 default=0, min_value=1, max_value=60, description=BAN_PROTECTION_MINUTE_DESCRIPTION)
                             ):
        language = LanguageManager(locale=inter.guild_locale)
        anti_nuke = AntiNukeTable(guild_id=inter.guild.id)
        await anti_nuke.load()
        #
        # if anti_nuke.block_role_id == role.id:
        #     response = language.get_embed_data(json_key='anti_nuke_block_role_error')
        # else:
        #     response = language.get_embed_data(json_key='anti_nuke_block_role')
        #     anti_nuke.block_role_id = role.id
        #     await anti_nuke.update()

        # await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(AntiNuke(client))
