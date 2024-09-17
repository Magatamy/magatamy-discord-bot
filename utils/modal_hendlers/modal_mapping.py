from modules.enums import ModalID
from utils.modal_hendlers.modal_private_channel import (
    change_name, change_limit
)


def get_modal_actions():
    return {
        ModalID.CHANGE_NAME.value: change_name,
        ModalID.CHANGE_LIMIT.value: change_limit
    }
