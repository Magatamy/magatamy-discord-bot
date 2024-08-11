import os
import time

from disnake.ext import commands
from disnake import Activity, ActivityType, Intents
from modules.database import UsersTable, GuildSettingsTable, PrivateChannelsTable, SaturdayChannelsTable
from config import TEST_GUILDS, IGNORE_COG_NAMES, BOT_TOKEN, ACTIVITY_NAME, OWNER_IDS


def get_intents():
    intents = Intents.default()
    intents.members = True
    return intents


def check_db_tables():
    users_table = UsersTable()
    guild_settings = GuildSettingsTable()
    private_channels = PrivateChannelsTable()
    saturday_channels = SaturdayChannelsTable()

    users_table.create_table(users_table.columns)
    guild_settings.create_table(guild_settings.columns)
    private_channels.create_table(private_channels.columns)
    saturday_channels.create_table(saturday_channels.columns)


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
        chunk_guilds_at_startup=True
    )
    client.start_time = int(time.time())

    check_db_tables()
    load_extensions(client.load_extension)

    client.run(BOT_TOKEN)
