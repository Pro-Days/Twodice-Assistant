import threading
import asyncio
import main
import time
import datetime
from pytz import timezone


def run_discord_client():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main.run())
    loop.close()


if __name__ == "__main__":
    threading.Thread(target=run_discord_client).start()

    while True:
        current_time = datetime.datetime.now(timezone("Asia/Seoul")).time()
        if current_time.hour == 3 and current_time.minute == 20:
            threading.Thread(target=run_discord_client).start()
        time.sleep(60)
