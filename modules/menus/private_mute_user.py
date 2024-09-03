from disnake import SelectOption, Member, MessageInteraction
from disnake.ui import UserSelect, View

from modules.database import PrivateChannelsTable
from modules.managers import LanguageManager
from modules.generators import EmbedGenerator


class MenuMuteUser(UserSelect):
    def __init__(self, placeholder: str, channel_id: int):
        super().__init__(placeholder=placeholder)
        self.channel_id = channel_id

    async def callback(self, inter: MessageInteraction):
        user = self.values[0]
        language = LanguageManager(locale=inter.guild_locale)

        private_channel = PrivateChannelsTable(channel_id=self.channel_id)
        if not await private_channel.load(create=False):
            error_response = language.get_embed_data('error_private_not_exist')
            await inter.response.send_message(embed=EmbedGenerator(json_schema=error_response), ephemeral=True)
            return

        if inter.author.id != private_channel.owner_id:
            response = language.get_embed_data('error_private_author_not_owner')
        elif user.id == private_channel.owner_id:
            response = language.get_embed_data('error_private_mute_owner')
        else:
            permissions = inter.author.voice.channel.overwrites_for(user)
            if permissions.speak is False:
                permissions.speak = None
                response = language.get_embed_data('private_unmute_member')
            else:
                permissions.speak = False
                response = language.get_embed_data('private_mute_member')

            await inter.author.voice.channel.set_permissions(user, overwrite=permissions)
            if user.voice and user.voice.channel.id == self.channel_id:
                await user.move_to(inter.author.voice.channel)

        await inter.response.send_message(
            embed=EmbedGenerator(json_schema=response, member=user.display_name), ephemeral=True)


class MenuViewMuteUser(View):
    def __init__(self, channel_id: int, language: LanguageManager):
        super().__init__()
        placeholder = language.get_static('placeholder_menu_mute_user')
        self.add_item(MenuMuteUser(
            placeholder=placeholder, channel_id=channel_id))
