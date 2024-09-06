import random

from disnake import VoiceState, Member
from disnake.ext import commands

from modules.database import GuildSettingsTable, PrivateChannelsTable
from modules.generators import EmbedGenerator
from modules.managers import LanguageManager


class OnVoiceStateUpdate(commands.Cog):
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if before.channel and before.channel != after.channel:
            private_channel = PrivateChannelsTable(channel_id=before.channel.id)
            if await private_channel.load(create=False):
                if not before.channel.members:
                    await before.channel.delete()
                    await private_channel.delete()

                elif member.id == private_channel.owner_id:
                    members = [member for member in before.channel.members if not member.bot]

                    random_member: Member = random.choice(members)
                    private_channel.owner_id = random_member.id
                    await private_channel.update()

                    language = LanguageManager(locale=before.channel.guild.preferred_locale)
                    private_new_owner = language.get_embed_data('private_new_owner')
                    await before.channel.send(content=random_member.mention, embed=EmbedGenerator(
                        json_schema=private_new_owner, member=random_member.display_name))

        if after.channel:
            guild_setting = GuildSettingsTable(guild_id=after.channel.guild.id)
            await guild_setting.load_private()

            if after.channel.id == guild_setting.private_voice_channel_id and not member.bot:
                category = after.channel.guild.get_channel(guild_setting.private_category_id)
                voice_channel = await category.create_voice_channel(name=member.display_name)
                await member.move_to(channel=voice_channel)

                private_channel = PrivateChannelsTable(channel_id=voice_channel.id, owner_id=member.id)
                await private_channel.insert(data=private_channel.data_record)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnVoiceStateUpdate(client))
