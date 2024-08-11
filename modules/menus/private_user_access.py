from disnake import SelectOption, Member, MessageInteraction
from disnake.ui import Select, View

from modules.database import PrivateChannelsTable
from modules.managers import LanguageManager
from modules.generators import EmbedGenerator


class MenuUserAccess(Select):
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
            elif user.id == private_channel.owner_id:
                response = language.get_embed_data('error_private_access_owner')
            else:
                permissions = inter.author.voice.channel.overwrites_for(user)
                if permissions.connect is False:
                    permissions.connect = None
                    response = language.get_embed_data('private_give_access_member')
                else:
                    permissions.connect = False
                    response = language.get_embed_data('private_back_access_member')

                await inter.author.voice.channel.set_permissions(user, overwrite=permissions)
                if user.voice and user.voice.channel.id == self.channel_id:
                    await user.move_to(channel=None)

            await inter.response.send_message(
                embed=EmbedGenerator(json_schema=response, member=user.display_name), ephemeral=True)


class MenuViewUserAccess(View):
    def __init__(self, users: list[Member], channel_id: int, language: LanguageManager):
        super().__init__()
        options = [SelectOption(label=user.display_name, value=str(user.id)) for user in users]
        placeholder = language.get_static('placeholder_menu_user_access')
        self.add_item(MenuUserAccess(
            placeholder=placeholder, options=options, users=users, channel_id=channel_id))
