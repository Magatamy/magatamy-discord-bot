import random

from disnake import VoiceState, Member
from disnake.ext import commands

from modules.redis import GuildSettings, PrivateChannels
from modules.generators import EmbedGenerator
from modules.managers import LanguageManager


class OnVoiceStateUpdate(commands.Cog):
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if before.channel and before.channel != after.channel:
            setting = GuildSettings(key=before.channel.guild.id)
            await setting.load()

            if before.channel.id == setting.private_voice_channel_id:
                return

            private_channel = PrivateChannels(key=before.channel.id)
            if await private_channel.load():
                if not before.channel.members:
                    await before.channel.delete()
                    await private_channel.delete()

                elif member.id == private_channel.owner_id:
                    members = [member for member in before.channel.members if not member.bot]

                    random_member: Member = random.choice(members)
                    private_channel.owner_id = random_member.id
                    await private_channel.save()

                    language = LanguageManager(locale=before.channel.guild.preferred_locale, language=setting.language)
                    private_new_owner = language.get_embed_data('private_new_owner')
                    await before.channel.send(content=random_member.mention, embed=EmbedGenerator(
                        json_schema=private_new_owner, member=random_member.display_name))

        if after.channel:
            setting = GuildSettings(key=after.channel.guild.id)
            await setting.load()

            if after.channel.id == setting.private_voice_channel_id and not member.bot:
                category = after.channel.guild.get_channel(setting.private_category_id)
                voice_channel = await category.create_voice_channel(name=member.display_name)
                await member.move_to(channel=voice_channel)

                private_channel = PrivateChannels(key=voice_channel.id)
                private_channel.owner_id = member.id
                await private_channel.save()


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnVoiceStateUpdate(client))
