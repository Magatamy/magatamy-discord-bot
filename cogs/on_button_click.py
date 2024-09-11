from disnake import MessageInteraction, InteractionResponse, PermissionOverwrite
from disnake.ext import commands
from time import time

from modules.generators import EmbedGenerator
from modules.redis import PrivateChannels, GuildSettings, Users
from modules.managers import LanguageManager, ButtonManager
from modules.enums import ButtonID
from modules.modals import ModalChangeLimit, ModalChangeName
from modules.menus import MenuViewKickUser, MenuViewGetOwner, MenuViewMuteUser, MenuViewUserAccess


class OnButtonClick(commands.Cog):
    CLICK_TIMEOUT = 10000

    @commands.Cog.listener()
    async def on_button_click(self, inter: MessageInteraction):
        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        language = LanguageManager(locale=inter.locale, language=settings.language)
        button_actions = {
            ButtonID.CHANGE_NAME.value: self.change_name,
            ButtonID.NEW_LIMIT.value: self.new_limit,
            ButtonID.USER_ACCESS.value: self.user_access,
            ButtonID.CLOSE_OPEN_ROOM.value: self.open_close_room,
            ButtonID.HIDE_SHOW_ROOM.value: self.hide_show_room,
            ButtonID.MUTE_USER.value: self.mute_user,
            ButtonID.KICK_USER.value: self.kick_user,
            ButtonID.GET_OWNER.value: self.get_owner,
            ButtonID.CLEAR_SETTING.value: self.clear_setting,
            ButtonID.MUTE_ALL_USER.value: self.mute_all_user
        }
        action = button_actions.get(inter.component.custom_id)
        if action:
            await action(inter, language)

    async def change_name(self, inter: MessageInteraction, language: LanguageManager):
        private_channel = await self.check_and_get_private(inter=inter, language=language)
        if not private_channel:
            return

        await inter.response.send_modal(ModalChangeName(language=language))

    async def new_limit(self, inter: MessageInteraction, language: LanguageManager):
        private_channel = await self.check_and_get_private(inter=inter, language=language)
        if not private_channel:
            return

        await inter.response.send_modal(ModalChangeLimit(language=language))

    async def user_access(self, inter: MessageInteraction, language: LanguageManager):
        private_channel = await self.check_and_get_private(inter=inter, language=language)
        if not private_channel:
            return

        response = language.get_embed_data('user_access_response')
        view = MenuViewUserAccess(channel_id=inter.author.voice.channel.id, language=language)

        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True, view=view)

    async def open_close_room(self, inter: MessageInteraction, language: LanguageManager):
        private_channel = await self.check_and_get_private(inter=inter, language=language)
        if not private_channel:
            return

        overwrite = inter.author.voice.channel.overwrites_for(inter.guild.default_role)
        if overwrite.connect is None:
            response = language.get_embed_data('close_room_response')
            overwrite.connect = False
        else:
            response = language.get_embed_data('open_room_response')
            overwrite.connect = None

        user = Users(key=inter.author.id)
        user.private_close = overwrite.connect
        await user.save()

        await inter.author.voice.channel.set_permissions(target=inter.guild.default_role, overwrite=overwrite)
        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)

    async def hide_show_room(self, inter: MessageInteraction, language: LanguageManager):
        private_channel = await self.check_and_get_private(inter=inter, language=language)
        if not private_channel:
            return

        overwrite = inter.author.voice.channel.overwrites_for(inter.guild.default_role)
        if overwrite.view_channel is None:
            response = language.get_embed_data('hide_room_response')
            overwrite.view_channel = False
        else:
            response = language.get_embed_data('show_room_response')
            overwrite.view_channel = None

        user = Users(key=inter.author.id)
        user.private_hide = overwrite.view_channel
        await user.save()

        await inter.author.voice.channel.set_permissions(target=inter.guild.default_role, overwrite=overwrite)
        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)

    async def mute_user(self, inter: MessageInteraction, language: LanguageManager):
        private_channel = await self.check_and_get_private(inter=inter, language=language)
        if not private_channel:
            return

        response = language.get_embed_data('mute_user_response')
        view = MenuViewMuteUser(channel_id=inter.author.voice.channel.id, language=language)

        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True, view=view)

    async def kick_user(self, inter: MessageInteraction, language: LanguageManager):
        private_channel = await self.check_and_get_private(inter=inter, language=language)
        if not private_channel:
            return

        response = language.get_embed_data('kick_user_response')
        view = MenuViewKickUser(channel_id=inter.author.voice.channel.id, language=language)

        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True, view=view)

    async def get_owner(self, inter: MessageInteraction, language: LanguageManager):
        private_channel = await self.check_and_get_private(inter=inter, language=language)
        if not private_channel:
            return

        response = language.get_embed_data('get_owner_response')
        view = MenuViewGetOwner(channel_id=inter.author.voice.channel.id, language=language)

        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True, view=view)

    async def clear_setting(self, inter: MessageInteraction, language: LanguageManager):
        private_channel = await self.check_and_get_private(inter=inter, language=language)
        if not private_channel:
            return

        user = Users(key=inter.author.id)
        await user.delete()

        overwrite = inter.author.voice.channel.overwrites_for(inter.guild.default_role)
        overwrite.connect = None
        overwrite.view_channel = None
        await inter.author.voice.channel.set_permissions(target=inter.guild.default_role, overwrite=overwrite)
        await inter.author.voice.channel.edit(user_limit=None)

        response = language.get_embed_data('clear_setting_response')
        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)

    async def mute_all_user(self, inter: MessageInteraction, language: LanguageManager):
        private_channel = await self.check_and_get_private(inter=inter, language=language)
        if not private_channel:
            return

        overwrite = inter.author.voice.channel.overwrites_for(inter.guild.default_role)
        overwrite_owner = inter.author.voice.channel.overwrites_for(inter.author)
        if overwrite.speak is False:
            overwrite.speak = None
            overwrite_owner.speak = None
            response = language.get_embed_data('unmute_all_user_response')
        else:
            overwrite.speak = False
            overwrite_owner.speak = True
            response = language.get_embed_data('mute_all_user_response')

        await inter.author.voice.channel.set_permissions(target=inter.author, overwrite=overwrite_owner)
        await inter.author.voice.channel.set_permissions(target=inter.guild.default_role, overwrite=overwrite)

        for member in inter.author.voice.channel.members:
            if member.id == inter.author.id:
                continue
            await member.move_to(member.voice.channel)

        user = Users(key=inter.author.id)
        user.private_mute_all = overwrite.speak
        await user.save()

        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)

    async def check_and_get_private(self, inter: MessageInteraction, language: LanguageManager) -> PrivateChannels | None:
        error_not_in_voice, error_not_in_private, error_not_is_owner, error_timeout = language.get_embed_data([
            'error_private_not_in_voice',
            'error_private_not_in_private',
            'error_channel_not_is_owner',
            'error_click_timeout'
        ])

        if not inter.author.voice:
            await inter.response.send_message(embed=EmbedGenerator(json_schema=error_not_in_voice), ephemeral=True)
            return

        private_channel = PrivateChannels(key=inter.author.voice.channel.id)
        if not await private_channel.load():
            await inter.response.send_message(embed=EmbedGenerator(json_schema=error_not_in_private), ephemeral=True)
            return

        if private_channel.owner_id != inter.author.id:
            await inter.response.send_message(embed=EmbedGenerator(json_schema=error_not_is_owner), ephemeral=True)
            return

        timestamp_now = int(time() * 1000)
        user = Users(key=inter.author.id)
        await user.load()

        if user.last_click_button_ts:
            timestamp_range = timestamp_now - user.last_click_button_ts
            if timestamp_range < self.CLICK_TIMEOUT:
                need_seconds = int((self.CLICK_TIMEOUT - timestamp_range) / 1000)
                await inter.response.send_message(
                    embed=EmbedGenerator(json_schema=error_timeout, range=need_seconds), ephemeral=True)
                return

        user.last_click_button_ts = timestamp_now
        await user.save()

        return private_channel


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnButtonClick(client))
