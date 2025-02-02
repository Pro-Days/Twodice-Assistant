import os
import bot
import time
import discord
import asyncio
import datetime
import platform
import traceback
import get_answer as ga
import update_data as ud
from pytz import timezone

os_name = platform.system()
if os_name == "Linux":
    ADMIN_ID = 407775594714103808
    ADMIN_CHANNEL_ID = 1244674283826053241
    LOG_CHANNEL_ID = 1244676938002468939
else:
    ADMIN_ID = 407775594714103808
    ADMIN_CHANNEL_ID = 1248628536311550045
    LOG_CHANNEL_ID = 1248628675134488637

discord_client = discord.Client(intents=discord.Intents.all())


@discord_client.event
async def on_ready():
    print(f"'{discord_client.user.name}' 로그인 성공 (ID: {discord_client.user.id})")
    await discord_bot.send_log(log_type=1, var=None)

    while True:
        current_time = datetime.datetime.now(timezone("Asia/Seoul")).time()
        if current_time.hour == 3 and current_time.minute == 20:
            await discord_client.close()
            break

        await asyncio.sleep(30)


@discord_client.event
async def on_message(message):
    if (message.channel.id == ADMIN_CHANNEL_ID) and (message.author.id == ADMIN_ID):
        await discord_bot.admin(message)

    elif message.content.startswith("!한월"):
        ans_json = await ga.get_ans(message)
        try:
            await discord_bot.hanwol(message, ans_json)
        except:
            await discord_bot.send(
                "죄송하지만 오류가 발생했어요\n다시 한번 말씀해주시겠어요?",
                message,
                error=traceback.format_exc(),
                log_type=5,
                ans_json=ans_json,
            )


def run():
    ud.update_data()
    global discord_bot
    discord_bot = bot.DiscordBot(discord_client)
    discord_client.run(os.getenv("DISCORD_TOKEN"))

    while True:
        current_time = datetime.datetime.now(timezone("Asia/Seoul")).time()
        if current_time.hour == 3 and current_time.minute == 20:
            break
        time.sleep(1)


if __name__ == "__main__":
    run()
