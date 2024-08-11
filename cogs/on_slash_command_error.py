from disnake import ApplicationCommandInteraction
from disnake.ext import commands


class OnSlashCommandError(commands.Cog):
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: ApplicationCommandInteraction, error: commands.CommandError):
        raise error


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnSlashCommandError(client))
