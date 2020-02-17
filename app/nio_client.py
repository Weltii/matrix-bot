from .utils import (get_last_batch, save_batch)
from .mod_processor import (process_command)
from nio import (AsyncClient, SyncResponse, RoomMessageText, LoginResponse)
import asyncio
from importlib import util
import sys
sys.path.append("./")


class BotClient(AsyncClient):
    def shutdown(self):
        self.run = False
        return "I will shut me down!"

    def process_input(self, input: str):
        output = "I don't have any idea what I can do with this command {}!"\
            .format(input)
        input.strip()
        if input.startswith("!"):
            if input.startswith("!bot"):
                command = input.replace("!bot", "").strip()
                func = self.command_mapping.get(command)
                if func:
                    output = func()
            else:
                output = process_command(input)
        return output

    async def run_sync_loop(self):
        while(self.run):
            sync_response: SyncResponse = await self.sync(30000)
            save_batch(sync_response.next_batch)
            if (len(sync_response.rooms.join) > 0):
                for room_id in sync_response.rooms.join:
                    for event in sync_response.rooms.join[room_id].timeline.events:
                        if hasattr(event, "body") and event.sender != self.user_id:
                            content = {
                                "body":
                                self.process_input(event.body),
                                "msgtype": "m.text"
                            }
                            await self.room_send(room_id, 'm.room.message', content)
        print("end of sync loop!")

    async def login_client(self, password):
        login_response = await self.login(password)
        print(login_response)  # add something when he failed!
        self.user_id = login_response.user_id
        self.next_batch = get_last_batch()

    async def logout_client(self):
        await self.logout()
        print("logout sucessfull!")

    async def run_client(self):
        await self.login_client(self.password)
        await self.run_sync_loop()
        await self.logout()
        await self.close()

    def __init__(self, home_server: str, user_name: str, password: str):
        AsyncClient.__init__(self, home_server, user_name)
        self.password = password
        self.run = True
        self.command_mapping = dict(
            shutdown=self.shutdown
        )
