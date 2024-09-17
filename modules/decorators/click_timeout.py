from functools import wraps
from time import time
from modules.generators import EmbedGenerator
from modules.redis import UsersClickButton


def click_timeout(timeout_duration: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(inter, language, *args, **kwargs):
            user = UsersClickButton(key=inter.author.id)
            time_to_live = await user.get_time_to_live()

            if time_to_live:
                error_timeout = language.get_embed_data('error_click_timeout')
                await inter.response.send_message(
                    embed=EmbedGenerator(json_schema=error_timeout, range=time_to_live), ephemeral=True)
                return

            user.last_click_button_ts = int(time() * 1000)
            await user.save(time_to_live=timeout_duration)

            return await func(inter, language, *args, **kwargs)
        return wrapper
    return decorator
