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
ACTIVITY_NAME = 'activity_name'
LANGUAGES_DEFAULT = 'default_language'  # Language name from language files
IGNORE_COG_NAMES = []  # List of COG names to ignore
OWNER_IDS = set()  # Set of bot owner IDs
TEST_GUILDS = []  # List of guild IDs
ERROR_LOG_CHANNEL = 1234567890  # Channel ID for error logging
