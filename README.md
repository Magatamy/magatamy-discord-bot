## Configuration Setup

Your bot requires a configuration file named `config.py`, which contains important parameters for its operation. Since the `config.py` file is included in `.gitignore` (to avoid being tracked by the repository), you need to create it manually in the root directory of your project.

### Template `config.py`

Create a file named `config.py` in the root directory of your project and add the following code, replacing the values with the appropriate ones for your bot:

```python
# config.py

BOT_TOKEN = 'your_bot_token'
REDIS_HOST = 'redis_server_address'
REDIS_PORT = 6379  # Default port for Redis
REDIS_PASSWORD = 'redis_server_password'
NUMBER_BD = 0 # Max number db 16 in default Redis config
ACTIVITY_NAME = 'activity_name'
LANGUAGES_DIRECTORY = 'languages' # Default directory in project
LANGUAGES_DEFAULT = 'default_language'  # Language name from language files
IGNORE_COG_NAMES = []  # List of COG names to ignore
OWNER_IDS = set()  # Set of bot owner IDs
TEST_GUILDS = []  # List of guild IDs
ERROR_LOG_CHANNEL = 1234567890  # Channel ID for error logging
```

## Redis Installation

To run the bot, Redis must be installed and configured properly. Follow these steps to install Redis:

### Ubuntu/Debian:

1. Install Redis:
    ```bush
    sudo apt install redis-server 
    ```
2. Enable Redis to start automatically on system boot:
    ```bush
    sudo systemctl enable redis-server
    ```
3. Start Redis:
    ```bush
    sudo systemctl start redis-server
    ```
   
### Windows:

1. Download Redis from the official GitHub repository: [Redis for Windows](https://github.com/microsoftarchive/redis/releases).
2. Extract and install Redis following the instructions provided.

### MacOS:

1. Install Redis using Homebrew:
    ```bush
    brew install redis
    ```
2. Start Redis:
    ```bush
    brew services start redis
    ```
   
## Required Libraries

Make sure you have the following Python libraries installed. You can install them by running the command below:
```bush
pip install -r requirements.txt
```

### Here is a list of the required libraries for your bot:

- `aiofiles` - For handling file operations asynchronously.
- `aiosqlite` - For asynchronous SQLite database operations.
- `asyncio` - For asynchronous programming.
- `disnake` - Main library for interacting with Discord.
- `htmlwebshot` - For taking screenshots of web pages. 
- `pytz` - For working with time zones.
- `redis` - For interacting with Redis.

## Running the Bot

Once you have created your config.py, installed Redis, and installed the required libraries, you can run the bot using:

```bush
python main.py
```

## Adding Custom Languages

To add your own language to the bot, follow these steps:

1. **Locate the Directory**: Find the `languages` directory in your project. This directory contains the translation files for different languages.

2. **Copy an Existing File**: Choose an existing language file that is closest to your target language. Copy this file and paste it in the `languages` directory. 

3. **Rename the File**: Rename the copied file to match the language key you want to use. The language key should be in the format specified by Disnake's localization documentation. You can find the list of language keys here: [Disnake Localization Documentation](https://docs.disnake.dev/en/latest/api/localization.html#locale).

4. **Translate the Text**: Open the new file and translate all the text within it to your desired language. Make sure to keep the format and structure of the file intact.

5. **Update `config.py`**: In your `config.py`, set `LANGUAGES_DEFAULT` to the key of your new language file if you want to use it as the default.

```python
# config.py

LANGUAGES_DEFAULT = 'your_language_key' # Replace with the key of your new language file
```

## Contact

For any questions or support, please contact:

- **Discord**: mrbloodycat
- **Discord Server**: [Magatamy Dev](https://discord.gg/KCSCXzuPs7)
