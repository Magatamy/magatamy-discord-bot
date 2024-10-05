from disnake import MessageInteraction

from modules.managers import LanguageManager
from modules.decorators import click_timeout


@click_timeout(timeout_duration=3)
async def change_title(inter: MessageInteraction, language: LanguageManager):
    pass


@click_timeout(timeout_duration=3)
async def change_description(inter: MessageInteraction, language: LanguageManager):
    pass


@click_timeout(timeout_duration=3)
async def change_footer(inter: MessageInteraction, language: LanguageManager):
    pass


@click_timeout(timeout_duration=3)
async def change_color(inter: MessageInteraction, language: LanguageManager):
    pass


@click_timeout(timeout_duration=3)
async def change_end_time(inter: MessageInteraction, language: LanguageManager):
    pass


@click_timeout(timeout_duration=3)
async def change_winners(inter: MessageInteraction, language: LanguageManager):
    pass


@click_timeout(timeout_duration=3)
async def change_winner_role(inter: MessageInteraction, language: LanguageManager):
    pass


@click_timeout(timeout_duration=3)
async def change_winner_msg(inter: MessageInteraction, language: LanguageManager):
    pass


@click_timeout(timeout_duration=3)
async def create_giveaway(inter: MessageInteraction, language: LanguageManager):
    pass


