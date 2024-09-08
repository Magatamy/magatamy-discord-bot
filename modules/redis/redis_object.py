import redis as sync_redis
import redis.asyncio as async_redis

from time import gmtime
from config import REDIS_HOST, REDIS_POST


class RedisObject:
    redis = async_redis.Redis(host=REDIS_HOST, port=REDIS_POST)

    def __init__(self, category: str, key: str | int = None):
        self._category = category
        self._key = key
        self._update_data = {}
        self._data = {}

    def check_fields(self):
        redis = sync_redis.Redis(host=REDIS_HOST, port=REDIS_POST)

        keys_to_check = redis.keys(f'{self._category}:*')
        all_attributes = [
            value for key, value in self.__class__.__dict__.items()
            if not key.startswith('__') and not callable(value) and not isinstance(value, property)
        ]

        for key in keys_to_check:
            key = key.decode('utf-8')
            fields = redis.hkeys(key)
            fields = [field.decode('utf-8') for field in fields]

            fields_to_remove = [field for field in fields if field not in all_attributes]
            if fields_to_remove:
                redis.hdel(key, *fields_to_remove)
                print(f'Fields to remove from {key}: {fields_to_remove}')

        redis.close()

    @staticmethod
    def __process_value(value):
        value = value.decode('utf-8')
        if value == 'True':
            return True
        elif value == 'False':
            return False
        elif value.isdigit():
            return int(value)
        elif value == 'None':
            return None
        else:
            return value

    def __convert_update_data(self):
        converted_data = {}
        for key, value in self._update_data.items():
            if isinstance(value, bool):
                converted_data[key] = 'True' if value else 'False'
            elif value is None:
                converted_data[key] = 'None'
            else:
                converted_data[key] = value

        return converted_data

    async def load(self, key: str | int = None) -> bool:
        key = self._key if key is None else key
        result = await self.redis.hgetall(name=f'{self._category}:{key}')
        self._data = {k.decode('utf-8'): self.__process_value(v) for k, v in result.items()}

        if self._data:
            return True

    async def load_all(self, limit: int = 100) -> bool:
        self._data = {}
        all_keys = []
        cursor = 0

        while True:
            cursor, keys = await self.redis.scan(cursor, match=f'{self._category}:*', count=limit)
            all_keys.extend(keys)
            if cursor == 0:
                break

        for key in all_keys:
            key = key.decode('utf-8')
            result = await self.redis.hgetall(key)
            self._data = {k.decode('utf-8'): self.__process_value(v) for k, v in result.items()}

        if self._data:
            return True

    async def load_for_time(self, range_ms: int, timestamp_key: str, limit: int = 100) -> bool:
        timestamp_by_range = int(gmtime() * 1000) - range_ms
        self._data = {}
        all_keys = []
        cursor = 0

        while True:
            cursor, keys = await self.redis.scan(cursor, match=f'{self._category}:*')
            all_keys.extend(keys)
            if cursor == 0:
                break

        for key in all_keys:
            key = key.decode('utf-8')
            result = await self.redis.hgetall(key)
            data = {k.decode('utf-8'): self.__process_value(v) for k, v in result.items()}

            timestamp = data.get(timestamp_key)
            if timestamp and isinstance(timestamp, int) and timestamp >= timestamp_by_range:
                self._data[key] = data

        if limit:
            self._data = self._data[:limit]

        if self._data:
            return True

    async def load_sorted(self, sort_field: str, limit: int = 100):
        self._data = {}
        all_keys = []
        cursor = 0

        while True:
            cursor, keys = await self.redis.scan(cursor, match=f'{self._category}:*')
            all_keys.extend(keys)
            if cursor == 0:
                break

        for key in all_keys:
            key = key.decode('utf-8')
            result = await self.redis.hgetall(key)
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
        result = await self.redis.hset(f'{self._category}:{key}', mapping=self.__convert_update_data())

        if result:
            return True

    async def delete(self, key: str | int = None) -> bool:
        key = self._key if key is None else key
        result = await self.redis.delete(key)

        if result:
            return True
