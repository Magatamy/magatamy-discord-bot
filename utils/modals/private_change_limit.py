from disnake import TextInputStyle
from disnake.ui import Modal, TextInput

from modules.managers import LanguageManager
from modules.enums import ModalID, ModalInputID


class ModalChangeLimit(Modal):
    def __init__(self, language: LanguageManager):
        components = [
            TextInput(
                label=language.get_static('modal_label_change_limit'),
                placeholder=language.get_static('modal_placeholder_change_limit'),
                custom_id=ModalInputID.CHANGE_LIMIT.value,
                style=TextInputStyle.short,
                max_length=2,
            ),
        ]
        super().__init__(title=language.get_static('modal_title_change_limit'),
                         custom_id=ModalID.CHANGE_LIMIT.value,
                         components=components)
