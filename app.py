from app.nio_client import BotClient
from config import matrix as conf
from nio import (AsyncClient, SyncResponse, RoomMessageText, LoginResponse)
import asyncio
from importlib import util
import sys
sys.path.append("./")


bot: BotClient = BotClient(
    conf.get("homeserver"),
    conf.get("user_name"),
    conf.get("user_password")
)

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.run_client())
loop.close()
print("Bot are offline now! Goodby 👋")
