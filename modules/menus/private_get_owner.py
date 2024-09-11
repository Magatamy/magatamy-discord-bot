from disnake import SelectOption, Member, MessageInteraction
from disnake.ui import UserSelect, View

from modules.redis import PrivateChannels, GuildSettings
from modules.managers import LanguageManager
from modules.generators import EmbedGenerator


class MenuKickUser(UserSelect):
    def __init__(self, placeholder: str, channel_id: int):
        super().__init__(placeholder=placeholder)
        self.channel_id = channel_id

    async def callback(self, inter: MessageInteraction):
        user = self.values[0]

        settings = GuildSettings(key=inter.guild.id)
        await settings.load()
        language = LanguageManager(locale=inter.locale, language=settings.language)

        private_channel = PrivateChannels(key=self.channel_id)
        if not await private_channel.load():
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
            response = language.get_embed_data('error_private_get_owner')
        else:
            private_channel.owner_id = user.id
            await private_channel.save()

            response, new_owner = language.get_embed_data(['private_get_owner_member', 'private_new_owner'])
            await user.voice.channel.send(
                content=user.mention, embed=EmbedGenerator(json_schema=new_owner, member=user.display_name))

            await inter.response.send_message(
                embed=EmbedGenerator(json_schema=response, member=user.display_name), ephemeral=True)

            overwrite = inter.author.voice.channel.overwrites_for(inter.guild.default_role)
            if overwrite.speak is False:
                overwrite_old_owner = inter.author.voice.channel.overwrites_for(inter.author)
                overwrite_new_owner = inter.author.voice.channel.overwrites_for(user)
                overwrite_old_owner.speak = None
                overwrite_new_owner.speak = True
                await inter.author.voice.channel.set_permissions(target=inter.author, overwrite=overwrite_old_owner)
                await inter.author.voice.channel.set_permissions(target=user, overwrite=overwrite_new_owner)
                await user.move_to(user.voice.channel)
                await inter.author.move_to(inter.author.voice.channel)

            return

        await inter.response.send_message(
            embed=EmbedGenerator(json_schema=response, member=user.display_name), ephemeral=True)


class MenuViewGetOwner(View):
    def __init__(self, channel_id: int, language: LanguageManager):
        super().__init__()
        placeholder = language.get_static('placeholder_menu_get_user')
        self.add_item(MenuKickUser(
            placeholder=placeholder, channel_id=channel_id))
