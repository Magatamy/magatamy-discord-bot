from modules.redis.redis_object import RedisObject

CATEGORY_NAME = 'giveaway'


class Giveaway(RedisObject):
    __title_attribute = 'title'
    __description_attribute = 'description'
    __footer_text_attribute = 'footer_text'
    __color_embed_attribute = 'color_embed'
    __end_timestamp_attribute = 'end_timestamp'
    __winners_attribute = 'count_winners'
    __winner_role_id_attribute = 'winner_role_id'
    __message_to_winner_attribute = 'message_to_winner'
    __participants_attribute = 'participants'

    def __init__(self, key: int = None):
        """key is message_id"""
        self.key = key
        super().__init__(category=CATEGORY_NAME, key=key)

    @property
    def title(self) -> str:
        return self._data.get(self.__title_attribute)

    @title.setter
    def title(self, value: str):
        self._data[self.__title_attribute] = value

    @property
    def description(self) -> str:
        return self._data.get(self.__description_attribute)

    @description.setter
    def description(self, value: str):
        self._data[self.__description_attribute] = value

    @property
    def winners(self) -> str:
        return self._data.get(self.__winners_attribute)

    @winners.setter
    def winners(self, value: str):
        self._data[self.__winners_attribute] = value

    @property
    def status(self) -> int:
        return self._data.get(self.__status_attribute)

    @status.setter
    def status(self, value: int):
        self._data[self.__status_attribute] = value

    @property
    def timestamp(self) -> int:
        return self._data.get(self.__end_timestamp_attribute)

    @timestamp.setter
    def timestamp(self, value: int):
        self._data[self.__end_timestamp_attribute] = value

    @property
    def winner_role_id(self) -> int:
        return self._data.get(self.__winner_role_id_attribute)

    @winner_role_id.setter
    def winner_role_id(self, value: int):
        self._data[self.__winner_role_id_attribute] = value

    @property
    def participants(self) -> str:
        return self._data.get(self.__participants_attribute)

    @participants.setter
    def participants(self, value: str):
        self._data[self.__participants_attribute] = value

    @property
    def message_to_winner(self) -> str:
        return self._data.get(self.__message_to_winner_attribute)

    @message_to_winner.setter
    def message_to_winner(self, value: str):
        self._data[self.__message_to_winner_attribute] = value

    @property
    def color_embed(self) -> str:
        return self._data.get(self.__color_embed_attribute)

    @color_embed.setter
    def color_embed(self, value: str):
        self._data[self.__color_embed_attribute] = value

    @property
    def footer_text(self) -> str:
        return self._data.get(self.__footer_text_attribute)

    @footer_text.setter
    def footer_text(self, value: str):
        self._data[self.__footer_text_attribute] = value
