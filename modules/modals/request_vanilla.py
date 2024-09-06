from disnake import TextInputStyle
from disnake.ui import Modal, TextInput

from modules.managers import LanguageManager
from modules.enums import ModalID, ModalInputID


class ModalRequestVanilla(Modal):
    def __init__(self, language: LanguageManager):
        components = [
            TextInput(
                label=language.get_static('modal_label_request_vanilla_name'),
                placeholder=language.get_static('modal_placeholder_request_vanilla_name'),
                custom_id=ModalInputID.REQUEST_VANILLA_NAME.value,
                style=TextInputStyle.short,
                max_length=48
            ),
            TextInput(
                label=language.get_static('modal_label_request_vanilla_nickname'),
                placeholder=language.get_static('modal_placeholder_request_vanilla_nickname'),
                custom_id=ModalInputID.REQUEST_VANILLA_NICKNAME.value,
                style=TextInputStyle.short,
                max_length=48
            ),
            TextInput(
                label=language.get_static('modal_label_request_vanilla_info'),
                placeholder=language.get_static('modal_placeholder_request_vanilla_info'),
                custom_id=ModalInputID.REQUEST_VANILLA_INFO.value,
                style=TextInputStyle.paragraph
            ),
            TextInput(
                label=language.get_static('modal_label_request_vanilla_action'),
                placeholder=language.get_static('modal_placeholder_request_vanilla_action'),
                custom_id=ModalInputID.REQUEST_VANILLA_ACTION.value,
                style=TextInputStyle.paragraph
            ),
            TextInput(
                label=language.get_static('modal_label_request_vanilla_rule'),
                placeholder=language.get_static('modal_placeholder_request_vanilla_rule'),
                custom_id=ModalInputID.REQUEST_VANILLA_RULE.value,
                style=TextInputStyle.paragraph
            ),
        ]
        super().__init__(title=language.get_static('modal_title_request_vanilla'),
                         custom_id=ModalID.REQUEST_VANILLA.value,
                         components=components)
