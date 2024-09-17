from modules.managers import ButtonManager
from modules.enums import ButtonID, Emoji


def get_components():
    buttons = ButtonManager()
    buttons.add_button(custom_id=ButtonID.CHANGE_NAME.value, emoji=Emoji.CHANGE_NAME.value)
    buttons.add_button(custom_id=ButtonID.NEW_LIMIT.value, emoji=Emoji.NEW_LIMIT.value)
    buttons.add_button(custom_id=ButtonID.KICK_USER.value, emoji=Emoji.KICK_USER.value)
    buttons.add_button(custom_id=ButtonID.GET_OWNER.value, emoji=Emoji.GET_OWNER.value)
    buttons.add_button(custom_id=ButtonID.CLEAR_SETTING.value, emoji=Emoji.CLEAR_SETTING.value)
    buttons.add_button(custom_id=ButtonID.USER_ACCESS.value, emoji=Emoji.USER_ACCESS.value)
    buttons.add_button(custom_id=ButtonID.CLOSE_OPEN_ROOM.value, emoji=Emoji.CLOSE_OPEN_ROOM.value)
    buttons.add_button(custom_id=ButtonID.HIDE_SHOW_ROOM.value, emoji=Emoji.HIDE_SHOW_ROOM.value)
    buttons.add_button(custom_id=ButtonID.MUTE_USER.value, emoji=Emoji.MUTE_USER.value)
    buttons.add_button(custom_id=ButtonID.MUTE_ALL_USER.value, emoji=Emoji.MUTE_ALL_USER.value)

    return buttons.components
