from enum import Enum


class ButtonID(Enum):
    CHANGE_NAME = "b-0"
    NEW_LIMIT = "b-1"
    USER_ACCESS = "b-2"
    CLOSE_OPEN_ROOM = "b-3"
    MUTE_USER = "b-4"
    KICK_USER = "b-5"
    GET_OWNER = "b-6"
    HIDE_SHOW_ROOM = "b-7"
    CLEAR_SETTING = "b-8"
    MUTE_ALL_USER = "b-9"
    CHANGE_TITLE = "b-10"
    CHANGE_DESCRIPTION = "b-11"
    CHANGE_FOOTER = "b-12"
    CHANGE_COLOR = "b-13"
    CHANGE_END_TIME = "b-14"
    CHANGE_WINNERS = "b-15"
    CHANGE_WINNER_ROLE = "b-16"
    CHANGE_WINNER_MSG = "b-17"
    CREATE_GIVEAWAY = "b-18"
