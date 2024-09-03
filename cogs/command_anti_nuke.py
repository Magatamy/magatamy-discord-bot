from datetime import time as datetime
from disnake import ApplicationCommandInteraction, Role
from disnake.ext import commands

from modules.managers import Localized, LanguageManager
from modules.generators import EmbedGenerator
from modules.database import AntiNukeTable

COMMAND_NAME = Localized('anti_nuke_name')
BLOCK_ROLE_NAME = Localized('anti_nuke_block_role_name')
BLOCK_ROLE_DESCRIPTION = Localized('anti_nuke_block_role_description')
BAN_PROTECTION_NAME = Localized('anti_nuke_ban_protection_name')
BAN_PROTECTION_DESCRIPTION = Localized('anti_nuke_ban_protection_description')
BAN_PROTECTION_COUNT_DESCRIPTION = Localized('anti_nuke_ban_protection_count_description')
BAN_PROTECTION_TIME_DESCRIPTION = Localized('anti_nuke_ban_protection_time_description')
KICK_PROTECTION_NAME = Localized('anti_nuke_kick_protection_name')
KICK_PROTECTION_DESCRIPTION = Localized('anti_nuke_kick_protection_description')
KICK_PROTECTION_COUNT_DESCRIPTION = Localized('anti_nuke_kick_protection_count_description')
KICK_PROTECTION_TIME_DESCRIPTION = Localized('anti_nuke_kick_protection_time_description')


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

    @anti_nuke.sub_command(name=BAN_PROTECTION_NAME, description=BAN_PROTECTION_DESCRIPTION)
    async def ban_protection(
            self,
            inter: ApplicationCommandInteraction,
            count: int = commands.Param(min_value=1, max_value=100, description=BAN_PROTECTION_COUNT_DESCRIPTION),
            time: int = commands.Param(min_value=1, max_value=86400, description=BAN_PROTECTION_TIME_DESCRIPTION)
    ):
        language = LanguageManager(locale=inter.guild_locale)
        anti_nuke = AntiNukeTable(guild_id=inter.guild.id)
        await anti_nuke.load()
        anti_nuke.timeout_for_ban = datetime(second=time)
        anti_nuke.ban_protection_count = count
        await anti_nuke.update()

        response = language.get_embed_data(json_key='anti_nuke_ban_protection')
        await inter.response.send_message(
            embed=EmbedGenerator(json_schema=response, time=time, count=count), ephemeral=True)

    @anti_nuke.sub_command(name=KICK_PROTECTION_NAME, description=KICK_PROTECTION_DESCRIPTION)
    async def kick_protection(
            self,
            inter: ApplicationCommandInteraction,
            count: int = commands.Param(min_value=1, max_value=100, description=KICK_PROTECTION_COUNT_DESCRIPTION),
            time: int = commands.Param(min_value=1, max_value=86400, description=KICK_PROTECTION_TIME_DESCRIPTION)
    ):
        language = LanguageManager(locale=inter.guild_locale)
        anti_nuke = AntiNukeTable(guild_id=inter.guild.id)
        await anti_nuke.load()
        anti_nuke.timeout_for_kick = datetime(second=time)
        anti_nuke.kick_protection_count = count
        await anti_nuke.update()

        response = language.get_embed_data(json_key='anti_nuke_kick_protection')
        await inter.response.send_message(
            embed=EmbedGenerator(json_schema=response, time=time, count=count), ephemeral=True)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(AntiNuke(client))
