from disnake import ApplicationCommandInteraction, ButtonStyle
from disnake.ext import commands
from time import time

from modules.managers import Localized, LanguageManager, ButtonManager
from modules.generators import EmbedGenerator
from modules.redis import GuildSettings
from modules.enums import ButtonID, Emoji

COMMAND_NAME = Localized('create_giveaway_name')
COMMAND_DESCRIPTION = Localized('create_giveaway_description')


class CreateGiveaway(commands.Cog):
    @commands.slash_command(name=COMMAND_NAME, description=COMMAND_DESCRIPTION)
    @commands.cooldown(rate=2, per=10)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def create_giveaway(self, inter: ApplicationCommandInteraction):
        settings = GuildSettings(key=inter.guild.id)
        await settings.load()

        language = LanguageManager(locale=inter.locale, language=settings.language)
        settings, example = language.get_embed_data(json_key=['create_giveaway_settings', 'create_giveaway_example'])
        title, description, footer_text, color_embed, create_text = language.get_static(text_key=[
            'giveaway_example_title',
            'giveaway_example_description',
            'giveaway_example_footer_text',
            'giveaway_example_color_embed',
            'giveaway_create'
        ])

        end_time = int(time()) + 3600

        settings_embed = EmbedGenerator(json_schema=settings)
        example_embed = EmbedGenerator(
            json_schema=example, title=title, description=description, footer_text=footer_text, color_embed=color_embed,
            end_time=end_time, count_winners=1, count_participants=0)

        buttons_line_1 = ButtonManager()
        buttons_line_1.add_button(custom_id=ButtonID.CHANGE_TITLE.value, emoji=Emoji.CHANGE_NAME.value)
        buttons_line_1.add_button(custom_id=ButtonID.CHANGE_DESCRIPTION.value, emoji=Emoji.DESCRIPTION.value)
        buttons_line_1.add_button(custom_id=ButtonID.CHANGE_FOOTER.value, emoji=Emoji.BOTTOM.value)
        buttons_line_1.add_button(custom_id=ButtonID.CHANGE_COLOR.value, emoji=Emoji.COLOR.value)

        buttons_line_2 = ButtonManager()
        buttons_line_2.add_button(custom_id=ButtonID.CHANGE_END_TIME.value, emoji=Emoji.TIME.value)
        buttons_line_2.add_button(custom_id=ButtonID.CHANGE_WINNERS.value, emoji=Emoji.WINNERS.value)
        buttons_line_2.add_button(custom_id=ButtonID.CHANGE_WINNER_ROLE.value, emoji=Emoji.GET_OWNER.value)
        buttons_line_2.add_button(custom_id=ButtonID.CHANGE_WINNER_MSG.value, emoji=Emoji.MESSAGE.value)

        buttons_line_3 = ButtonManager()
        buttons_line_3.add_button(custom_id=ButtonID.CREATE_GIVEAWAY.value, label=create_text, style=ButtonStyle.green)

        await inter.response.send_message(
            embeds=[example_embed, settings_embed],
            components=[buttons_line_1.components, buttons_line_2.components, buttons_line_3.components],
            ephemeral=True
        )


def setup(client: commands.AutoShardedInteractionBot):
    client.add_cog(CreateGiveaway(client))
