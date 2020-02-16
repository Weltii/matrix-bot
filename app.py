from app.nio_client import BotClient
from nio import (AsyncClient, SyncResponse, RoomMessageText, LoginResponse)
import asyncio
from importlib import util
import sys
sys.path.append("./")


bot: BotClient = BotClient(
    "https://matrix.org",
    "weltiimore",
    "JmvAkL4fEDN4NhXUNAWY8Scwvt37by6Gw9zPu6d4rDEV9ASxCe85sLkG6pCXCSgj"
)

loop = asyncio.get_event_loop()
loop.run_until_complete(bot.run_client())
loop.close()
print("Bot are offline now! Goodby 👋")
