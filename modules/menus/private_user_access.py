from disnake import SelectOption, Member, MessageInteraction
from disnake.ui import Select, View, UserSelect

from modules.database import PrivateChannelsTable, GuildSettingsTable
from modules.managers import LanguageManager
from modules.generators import EmbedGenerator


class MenuUserAccess(UserSelect):
    def __init__(self, placeholder: str, channel_id: int):
        super().__init__(placeholder=placeholder)
        self.channel_id = channel_id

    async def callback(self, inter: MessageInteraction):
        user = self.values[0]

        settings = GuildSettingsTable(guild_id=inter.guild.id)
        await settings.load()
        language = LanguageManager(locale=inter.locale, language=settings.language)

        private_channel = PrivateChannelsTable(channel_id=self.channel_id)
        if not await private_channel.load(create=False):
            error_response = language.get_embed_data('error_private_not_exist')
            await inter.response.send_message(embed=EmbedGenerator(json_schema=error_response), ephemeral=True)
            return

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
    def __init__(self, channel_id: int, language: LanguageManager):
        super().__init__()
        placeholder = language.get_static('placeholder_menu_user_access')
        self.add_item(MenuUserAccess(placeholder=placeholder, channel_id=channel_id))
