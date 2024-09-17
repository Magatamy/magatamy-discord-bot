import os
import time

from disnake.ext import commands
from disnake import Activity, ActivityType, Intents
from config import TEST_GUILDS, IGNORE_COG_NAMES, BOT_TOKEN, ACTIVITY_NAME, OWNER_IDS


def get_intents():
    intents = Intents.default()
    intents.members = True
    return intents


def load_extensions(load_extension: commands.AutoShardedInteractionBot.load_extensions):
    for root, dirs, files in os.walk('cogs'):
        py_files = [file[:-3] for file in files if file.endswith(".py")]

        for file in py_files:
            if file in IGNORE_COG_NAMES:
                continue

            file_path = os.path.relpath(path=str(os.path.join(root, file)))
            path_name = str(file_path.replace(os.sep, "."))

            load_extension(path_name)


if __name__ == '__main__':
    client = commands.AutoShardedInteractionBot(
        owner_ids=OWNER_IDS,
        test_guilds=TEST_GUILDS,
        activity=Activity(name=ACTIVITY_NAME, type=ActivityType.playing),
        intents=get_intents(),
        reload=True,
        chunk_guilds_at_startup=True
    )
    client.start_time = int(time.time() * 1000)
    load_extensions(client.load_extension)
    client.run(BOT_TOKEN)
