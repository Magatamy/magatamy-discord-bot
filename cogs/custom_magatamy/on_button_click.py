from mcrcon import MCRcon
from config import custom_magatamy_request_vanilla_role, magatamy_host, magatamy_port, magatamy_password
from disnake import MessageInteraction, InteractionResponse, PermissionOverwrite, Colour
from disnake.ext import commands

from modules.generators import EmbedGenerator
from modules.database import RequestVanilla
from modules.managers import LanguageManager
from modules.enums import ButtonID, RequestStatus
from modules.modals import ModalRequestVanilla
from modules.menus import MenuViewKickUser, MenuViewGetOwner, MenuViewMuteUser, MenuViewUserAccess


class OnButtonClickMagatamy(commands.Cog):
    @commands.Cog.listener()
    async def on_button_click(self, inter: MessageInteraction):
        language = LanguageManager(locale=inter.locale)
        button_actions = {
            ButtonID.POST_REQUEST_VANILLA.value: self.request_vanilla,
            ButtonID.ACCEPT_REQUEST_VANILLA.value: self.accept_request_vanilla,
            ButtonID.REJECT_REQUEST_VANILLA.value: self.reject_request_vanilla
        }
        action = button_actions.get(inter.component.custom_id)
        if action:
            await action(inter, language)

    @staticmethod
    async def request_vanilla(inter: MessageInteraction, language: LanguageManager):
        request = RequestVanilla(member_id=inter.author.id)
        if await request.load(create=False) and request.status != RequestStatus.REJECTED.value:
            if request.status == RequestStatus.ACCEPTED.value:
                response = language.get_embed_data('request_vanilla_accepted')
            else:
                response = language.get_embed_data('request_vanilla_under_review')

            await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)
            return

        await inter.response.send_modal(ModalRequestVanilla(language=language))

    @staticmethod
    async def reject_request_vanilla(inter: MessageInteraction, language: LanguageManager):
        embed = inter.message.embeds[0]
        member = inter.guild.get_member(int(embed.title))

        response = language.get_embed_data('reject_request_vanilla')
        await member.send(embed=EmbedGenerator(json_schema=response))

        request = RequestVanilla(member_id=int(embed.title))
        await request.load()
        request.status = RequestStatus.REJECTED.value
        await request.update()

        embed.title = language.get_static('reject_request_label') + inter.author.name
        embed.colour = Colour.red()
        await inter.message.edit(embed=embed, components=None)

    @staticmethod
    async def accept_request_vanilla(inter: MessageInteraction, language: LanguageManager):
        embed = inter.message.embeds[0]
        member = inter.guild.get_member(int(embed.title))

        response = language.get_embed_data('accept_request_vanilla')
        await member.send(embed=EmbedGenerator(json_schema=response))

        request = RequestVanilla(member_id=int(embed.title))
        await request.load()
        request.status = RequestStatus.ACCEPTED.value
        await request.update()

        embed.title = language.get_static('accept_request_label') + inter.author.name
        embed.colour = Colour.green()
        await inter.message.edit(embed=embed, components=None)

        role = inter.guild.get_role(custom_magatamy_request_vanilla_role)
        await member.add_roles(role)

        with MCRcon(magatamy_host, magatamy_password, magatamy_port) as mcr:
            _ = mcr.command(f'sg removeguest {request.nickname}')


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnButtonClickMagatamy(client))
