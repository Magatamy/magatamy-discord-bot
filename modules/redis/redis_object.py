import redis as sync_redis
import redis.asyncio as async_redis

from time import time
from config import REDIS_HOST, REDIS_POST, REDIS_PASSWORD
from ..enums.convert_value import ConvertValue


class RedisObject:
    __redis = async_redis.Redis(host=REDIS_HOST, port=REDIS_POST, password=REDIS_PASSWORD)

    def __init__(self, category: str = 'default_category', key: str | int = None):
        self._category = category
        self._key = key
        self._data = {}

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        keys = list(self._data.keys())
        if self._iter_index < len(keys):
            key_value = keys[self._iter_index]
            new_object = type(self)(key=key_value.split(':')[-1])
            new_object._data = self._data[key_value]
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

    def __convert_data(self) -> dict:
        converted_data = {}
        for key, value in self._data.items():
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
        redis = sync_redis.Redis(host=REDIS_HOST, port=REDIS_POST)

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

    async def load_for_time(self, range_ms: int, timestamp_key: str, limit: int | None = 100) -> bool:
        timestamp_by_range = int(time() * 1000) - range_ms
        self._data = {}
        all_keys = await self.__get_all_keys()

        for key in all_keys:
            key = key.decode('utf-8')
            result = await self.__redis.hgetall(key)
            data = {k.decode('utf-8'): self.__process_value(v) for k, v in result.items()}

            timestamp = data.get(timestamp_key)
            if timestamp and isinstance(timestamp, int) and timestamp >= timestamp_by_range:
                self._data[key] = data

        if limit:
            self._data = self._data[:limit]

        if self._data:
            return True

    async def load_sorted(self, sort_field: str, limit: int | None = 100):
        self._data = {}
        all_keys = await self.__get_all_keys()

        for key in all_keys:
            key = key.decode('utf-8')
            result = await self.__redis.hgetall(key)
            data = {k.decode('utf-8'): self.__process_value(v) for k, v in result.items()}

            if sort_field in data:
                self._data.append(data)

        self._data = sorted(self._data, key=lambda x: x[sort_field])
        if limit:
            self._data = self._data[:limit]

        if self._data:
            return True

    async def save(self, key: str | int = None) -> bool:
        key = self._key if key is None else key
        result = await self.__redis.hset(f'{self._category}:{key}', mapping=self.__convert_data())

        if result:
            return True

    async def delete(self, key: str | int = None) -> bool:
        key = self._key if key is None else key
        result = await self.__redis.delete(f'{self._category}:{key}')

        if result:
            return True
