from disnake import SelectOption, Member, MessageInteraction
from disnake.ui import Select, View

from modules.database import PrivateChannelsTable
from modules.managers import LanguageManager
from modules.generators import EmbedGenerator


class MenuKickUser(Select):
    def __init__(self, placeholder: str, options: list, users: list[Member], channel_id: int):
        super().__init__(placeholder=placeholder, options=options)
        self.users = users
        self.channel_id = channel_id

    async def callback(self, inter: MessageInteraction):
        language = LanguageManager(locale=inter.guild_locale)

        private_channel = PrivateChannelsTable(channel_id=self.channel_id)
        if not await private_channel.load_data(create=False):
            error_response = language.get_embed_data('error_private_not_exist')
            await inter.response.send_message(embed=EmbedGenerator(json_schema=error_response), ephemeral=True)
            return

        item = int(self.values[0])
        for user in self.users:
            if user.id != item:
                continue

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
    def __init__(self, users: list[Member], channel_id: int, language: LanguageManager):
        super().__init__()
        users = [user for user in users if not user.bot]
        options = [SelectOption(label=user.display_name, value=str(user.id)) for user in users]
        placeholder = language.get_static('placeholder_menu_kick_user')
        self.add_item(MenuKickUser(
            placeholder=placeholder, options=options, users=users, channel_id=channel_id))
