from modules.enums import ButtonID
from utils.button_handlers.button_private_channel import (
    change_name, new_limit, user_access, open_close_room, hide_show_room, mute_user, kick_user, get_owner,
    clear_setting, mute_all_user
)
from utils.button_handlers.button_giveaway import (
    change_title, change_description, change_footer, change_color, change_end_time, change_winners, change_winner_role,
    change_winner_msg, create_giveaway
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
        ButtonID.MUTE_ALL_USER.value: mute_all_user,
        ButtonID.CHANGE_TITLE.value: change_title,
        ButtonID.CHANGE_DESCRIPTION.value: change_description,
        ButtonID.CHANGE_FOOTER.value: change_footer,
        ButtonID.CHANGE_COLOR.value: change_color,
        ButtonID.CHANGE_END_TIME.value: change_end_time,
        ButtonID.CHANGE_WINNERS.value: change_winners,
        ButtonID.CHANGE_WINNER_ROLE.value: change_winner_role,
        ButtonID.CHANGE_WINNER_MSG.value: change_winner_msg,
        ButtonID.CREATE_GIVEAWAY.value: create_giveaway
    }
