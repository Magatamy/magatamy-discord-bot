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
