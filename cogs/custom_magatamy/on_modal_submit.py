from config import custom_magatamy_request_channel
from disnake import ModalInteraction, ButtonStyle
from disnake.ext import commands

from modules.generators import EmbedGenerator
from modules.managers import LanguageManager, ButtonManager
from modules.enums import ModalID, ModalInputID, RequestStatus, ButtonID
from modules.database import RequestVanilla, GuildSettingsTable


class OnModalSubmitMagatamy(commands.Cog):
    @commands.Cog.listener()
    async def on_modal_submit(self, inter: ModalInteraction):
        settings = GuildSettingsTable(guild_id=inter.guild.id)
        await settings.load()
        language = LanguageManager(locale=inter.locale, language=settings.language)
        modal_actions = {
            ModalID.REQUEST_VANILLA.value: self.request_vanilla
        }
        action = modal_actions.get(inter.custom_id)
        if action:
            await action(inter, language)

    @staticmethod
    async def request_vanilla(inter: ModalInteraction, language: LanguageManager):
        name = inter.text_values.get(ModalInputID.REQUEST_VANILLA_NAME.value)
        nickname = inter.text_values.get(ModalInputID.REQUEST_VANILLA_NICKNAME.value)
        info = inter.text_values.get(ModalInputID.REQUEST_VANILLA_INFO.value)
        action = inter.text_values.get(ModalInputID.REQUEST_VANILLA_ACTION.value)
        rule = inter.text_values.get(ModalInputID.REQUEST_VANILLA_RULE.value)

        response, request_mod = language.get_embed_data(['request_vanilla_post', 'request_vanilla_mod'])
        accept_label, reject_label, label_name, label_nickname, label_info, label_action, label_rule = language.get_static([
            'request_vanilla_accept_label',
            'request_vanilla_reject_label',
            'modal_label_request_vanilla_name',
            'modal_label_request_vanilla_nickname',
            'modal_label_request_vanilla_info',
            'modal_label_request_vanilla_action',
            'modal_label_request_vanilla_rule'
        ])

        buttons = ButtonManager()
        buttons.add_button(custom_id=ButtonID.ACCEPT_REQUEST_VANILLA.value, label=accept_label, style=ButtonStyle.green)
        buttons.add_button(custom_id=ButtonID.REJECT_REQUEST_VANILLA.value, label=reject_label, style=ButtonStyle.red)

        request_channel = inter.guild.get_channel(custom_magatamy_request_channel)
        await request_channel.send(embed=EmbedGenerator(
            json_schema=request_mod, label_name=label_name, name=name, label_nickname=label_nickname, nickname=nickname,
            label_info=label_info, info=info, label_action=label_action, action=action,label_rule=label_rule, rule=rule,
            user_id=inter.author.id, user_mention=inter.author.mention, user_name=inter.author.name
        ), components=buttons.components)
        await inter.response.send_message(embed=EmbedGenerator(json_schema=response), ephemeral=True)

        request = RequestVanilla(member_id=inter.author.id)
        await request.load()
        request.status = RequestStatus.UNDER_REVIEW.value
        request.name_and_age = name
        request.nickname = nickname
        request.found_info = info
        request.action_on_server = action
        request.read_rule = rule
        await request.update()


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(OnModalSubmitMagatamy(client))
