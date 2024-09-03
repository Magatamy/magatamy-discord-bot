from disnake import SelectOption, Member, MessageInteraction
from disnake.ui import UserSelect, View

from modules.database import PrivateChannelsTable
from modules.managers import LanguageManager
from modules.generators import EmbedGenerator


class MenuKickUser(UserSelect):
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
        elif not user.voice:
            response = language.get_embed_data('error_private_menu_not_in_voice')
        elif user.voice.channel.id != self.channel_id:
            response = language.get_embed_data('error_private_menu_not_in_private')
        elif user.id == private_channel.owner_id:
            response = language.get_embed_data('error_private_kick_owner')
        else:
            await user.move_to(channel=None)
            response = language.get_embed_data('private_kick_member')

        await inter.response.send_message(
            embed=EmbedGenerator(json_schema=response, member=user.display_name), ephemeral=True)


class MenuViewKickUser(View):
    def __init__(self, channel_id: int, language: LanguageManager):
        super().__init__()
        placeholder = language.get_static('placeholder_menu_kick_user')
        self.add_item(MenuKickUser(
            placeholder=placeholder, channel_id=channel_id))
