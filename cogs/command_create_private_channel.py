from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from modules.managers import Localized, LanguageManager, ButtonManager
from modules.generators import EmbedGenerator
from modules.redis import GuildSettings
from modules.enums import ButtonID, Emoji

COMMAND_NAME = Localized('create_private_channel_name')
COMMAND_DESCRIPTION = Localized('create_private_channel_description')


class CreatePrivateChannel(commands.Cog):
    @commands.slash_command(name=COMMAND_NAME, description=COMMAND_DESCRIPTION)
    @commands.cooldown(rate=2, per=10)
    @commands.has_permissions(administrator=True)
    async def create_private_channel(self, inter: ApplicationCommandInteraction):
        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        language = LanguageManager(locale=inter.locale, language=settings.language)

        response, channel_setting = language.get_embed_data(['create_private_channel', 'private_channel_setting'])
        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)

        category_name, text_channel_name, voice_channel_name = language.get_static(
            ['private_category_name', 'private_text_channel_name', 'private_voice_channel_name'])
        category = await inter.guild.create_category(name=category_name)
        text_channel = await category.create_text_channel(name=text_channel_name)
        voice_channel = await category.create_voice_channel(name=voice_channel_name)

        settings.private_category_id = category.id
        settings.private_voice_channel_id = voice_channel.id
        await settings.save()

        buttons = ButtonManager()
        buttons.add_button(custom_id=ButtonID.CHANGE_NAME.value, emoji=Emoji.CHANGE_NAME.value)
        buttons.add_button(custom_id=ButtonID.NEW_LIMIT.value, emoji=Emoji.NEW_LIMIT.value)
        buttons.add_button(custom_id=ButtonID.CLOSE_OPEN_ROOM.value, emoji=Emoji.CLOSE_OPEN_ROOM.value)
        buttons.add_button(custom_id=ButtonID.HIDE_SHOW_ROOM.value, emoji=Emoji.HIDE_SHOW_ROOM.value)
        buttons.add_button(custom_id=ButtonID.KICK_USER.value, emoji=Emoji.KICK_USER.value)
        buttons.add_button(custom_id=ButtonID.USER_ACCESS.value, emoji=Emoji.USER_ACCESS.value)
        buttons.add_button(custom_id=ButtonID.MUTE_USER.value, emoji=Emoji.MUTE_USER.value)
        buttons.add_button(custom_id=ButtonID.GET_OWNER.value, emoji=Emoji.GET_OWNER.value)
        buttons.add_button(custom_id=ButtonID.CLEAR_SETTING.value, emoji=Emoji.CLEAR_SETTING.value)

        await text_channel.send(embed=EmbedGenerator(json_schema=channel_setting), components=buttons.components)


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(CreatePrivateChannel(client))
