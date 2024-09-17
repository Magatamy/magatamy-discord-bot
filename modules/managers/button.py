from disnake import ButtonStyle
from disnake.ui import Button
from modules.enums import Emoji


class ButtonManager:
    def __init__(self):
        self._buttons = []

    def add_button(self, custom_id: str, emoji: Emoji = None, label: str = None, style=ButtonStyle.gray):
        button = Button(custom_id=custom_id, emoji=emoji, label=label, style=style)
        self._buttons.append(button)

    @property
    def components(self):
        return self._buttons
