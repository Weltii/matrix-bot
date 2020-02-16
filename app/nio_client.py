from importlib import util
import asyncio
from nio import (AsyncClient, SyncResponse, RoomMessageText, LoginResponse)
from utils import (get_last_batch, save_batch)

response_string = "!mensa"


class BotClient(AsyncClient):
    async def run_sync_loop(self):
        while(True):
            sync_response: SyncResponse = await self.sync(30000)
            save_batch(sync_response.next_batch)
            if (len(sync_response.rooms.join) > 0):
                for room_id in sync_response.rooms.join:
                    for event in sync_response.rooms.join[room_id].timeline.events:
                        if hasattr(event, "body") and \
                                event.body.startswith(response_string) and \
                                event.sender != self.user_id:
                            response_body = event.body.replace(
                                response_string, "").strip()
                            content = {
                                "body": response_body,
                                "msgtype": "m.text"
                            }
                            await self.room_send(room_id, 'm.room.message', content)
                        elif event.sender != self.user_id:
                            response_body = event.body.replace(
                                response_string, "").strip()
                            content = {
                                "body": 'I don\'t understand {}!'.format(response_body),
                                "msgtype": "m.text"
                            }
                            await self.room_send(room_id, 'm.room.message', content)


    async def login_client(self, password):
        login_response = await self.login(password)
        print(login_response) # add something when he failed!
        self.user_id = login_response.user_id
        self.next_batch = get_last_batch()


    async def run_client(self):
        await self.login_client(self.password)
        await self.run_sync_loop()


    def __init__(self, home_server: str, user_name: str, password: str):
        AsyncClient.__init__(self, home_server, user_name)
        self.password = password