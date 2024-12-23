import redis as sync_redis
import redis.asyncio as async_redis

from time import time
from copy import deepcopy
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, NUMBER_BD
from modules.enums import ConvertValue

DEFAULT_CATEGORY_NAME = 'default_category'


class RedisObject:
    __redis = async_redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=NUMBER_BD)

    def __init__(self, category: str = DEFAULT_CATEGORY_NAME, key: str | int = None):
        self._category = category
        self._key = key
        self._data = {}
        self.__loaded_data = {}

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        keys = list(self._data.keys())
        if self._iter_index < len(keys):
            key_value = keys[self._iter_index]
            new_object = type(self)(key=key_value.split(':')[-1])
            new_object._data = self._data[key_value]
            new_object.__loaded_data = deepcopy(new_object._data)
            self._iter_index += 1
            return new_object
        else:
            raise StopIteration

    @staticmethod
    def __process_value(value) -> bool | int | str | None:
        value = value.decode('utf-8')
        if value == ConvertValue.TRUE.value:
            return True
        elif value == ConvertValue.FALSE.value:
            return False
        elif value.isdigit():
            return int(value)
        elif value == ConvertValue.NONE.value:
            return None
        else:
            return value

    @staticmethod
    def __convert_data(data) -> dict:
        converted_data = {}
        for key, value in data.items():
            if isinstance(value, bool):
                converted_data[key] = ConvertValue.TRUE.value if value else ConvertValue.FALSE.value
            elif value is None:
                converted_data[key] = ConvertValue.NONE.value
            else:
                converted_data[key] = value

        return converted_data

    async def __get_all_keys(self, limit: int = None) -> list:
        all_keys = []
        cursor = 0

        while True:
            cursor, keys = await self.__redis.scan(cursor, match=f'{self._category}:*', count=limit)
            all_keys.extend(keys)
            if cursor == 0:
                break

        return all_keys

    def check_fields(self):
        redis = sync_redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

        all_attributes = [
            value for key, value in self.__class__.__dict__.items()
            if not key.startswith('__') and not callable(value) and not isinstance(value, property)
        ]

        keys_to_check = redis.keys(f'{self._category}:*')
        for key in keys_to_check:
            key = key.decode('utf-8')
            fields = redis.hkeys(key)
            fields = [field.decode('utf-8') for field in fields]

            fields_to_remove = [field for field in fields if field not in all_attributes]
            if fields_to_remove:
                redis.hdel(key, *fields_to_remove)
                print(f'Fields to remove from {key}: {fields_to_remove}')

        redis.close()

    async def load(self, key: str | int = None) -> bool:
        key = self._key if key is None else key
        result = await self.__redis.hgetall(name=f'{self._category}:{key}')
        self._data = {k.decode('utf-8'): self.__process_value(v) for k, v in result.items()}
        self.__loaded_data = deepcopy(self._data)

        if self._data:
            return True

    async def load_all(self, limit: int | None = 100) -> bool:
        self._data = {}
        all_keys = await self.__get_all_keys(limit=limit)

        for key in all_keys:
            key = key.decode('utf-8')
            result = await self.__redis.hgetall(key)
            self._data[key] = {k.decode('utf-8'): self.__process_value(v) for k, v in result.items()}

        if self._data:
            return True

    async def load_for_time(self, time_range: int, timestamp_field: str, limit: int | None = 100) -> bool:
        timestamp_by_range = int(time() * 1000) - time_range
        self._data = {}
        all_keys = await self.__get_all_keys()

        for key in all_keys:
            key = key.decode('utf-8')
            result = await self.__redis.hgetall(key)
            data = {k.decode('utf-8'): self.__process_value(v) for k, v in result.items()}

            timestamp = data.get(timestamp_field)
            if timestamp and isinstance(timestamp, int) and timestamp >= timestamp_by_range:
                self._data[key] = data

        if limit:
            self._data = dict(list(self._data.items())[:limit])

        if self._data:
            return True

    async def load_sorted(self, sort_field: str, reverse_sorted: bool = False, limit: int | None = 100):
        self._data = {}
        all_keys = await self.__get_all_keys()

        for key in all_keys:
            key = key.decode('utf-8')
            result = await self.__redis.hgetall(key)
            data = {k.decode('utf-8'): self.__process_value(v) for k, v in result.items()}

            if sort_field in data:
                self._data[key] = data

        list_data = list(self._data.items())
        sorted_list_data = sorted(list_data, key=lambda item: item[1][sort_field], reverse=reverse_sorted)
        if limit:
            sorted_list_data = sorted_list_data[:limit]

        self._data = dict(sorted_list_data)

        if self._data:
            return True

    async def save(self, key: str | int = None, time_to_live: int = None) -> bool:
        key = self._key if key is None else key
        hash_key = f'{self._category}:{key}'

        changed_data = {
            key: self._data[key] for key in self._data
            if self._data[key] != self.__loaded_data.get(key)
        } if self.__loaded_data else self._data
        
        if not changed_data:
            return False

        result = await self.__redis.hset(name=hash_key, mapping=self.__convert_data(data=changed_data))
        if result and time_to_live:
            await self.__redis.expire(name=hash_key, time=time_to_live)

        if result:
            return True

    async def delete(self, key: str | int = None) -> bool:
        key = self._key if key is None else key
        result = await self.__redis.delete(f'{self._category}:{key}')

        if result:
            return True

    async def get_time_to_live(self, key: str | int = None) -> int:
        key = self._key if key is None else key
        ttl = await self.__redis.ttl(f'{self._category}:{key}')

        if ttl != -2:
            return ttl
