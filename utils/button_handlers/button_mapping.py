from modules.enums import ButtonID
from utils.button_handlers.button_private_channel import (
    change_name, new_limit, user_access, open_close_room, hide_show_room,
    mute_user, kick_user, get_owner, clear_setting, mute_all_user
)


def get_button_actions():
    return {
        ButtonID.CHANGE_NAME.value: change_name,
        ButtonID.NEW_LIMIT.value: new_limit,
        ButtonID.USER_ACCESS.value: user_access,
        ButtonID.CLOSE_OPEN_ROOM.value: open_close_room,
        ButtonID.HIDE_SHOW_ROOM.value: hide_show_room,
        ButtonID.MUTE_USER.value: mute_user,
        ButtonID.KICK_USER.value: kick_user,
        ButtonID.GET_OWNER.value: get_owner,
        ButtonID.CLEAR_SETTING.value: clear_setting,
        ButtonID.MUTE_ALL_USER.value: mute_all_user
    }
