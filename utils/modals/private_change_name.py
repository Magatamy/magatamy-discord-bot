from disnake import TextInputStyle
from disnake.ui import Modal, TextInput

from modules.managers import LanguageManager
from modules.enums import ModalID, ModalInputID


class ModalChangeName(Modal):
    def __init__(self, language: LanguageManager):
        components = [
            TextInput(
                label=language.get_static('modal_label_change_name'),
                placeholder=language.get_static('modal_placeholder_change_name'),
                custom_id=ModalInputID.CHANGE_NAME.value,
                style=TextInputStyle.short,
                max_length=99,
            ),
        ]
        super().__init__(title=language.get_static('modal_title_change_name'),
                         custom_id=ModalID.CHANGE_NAME.value,
                         components=components)
