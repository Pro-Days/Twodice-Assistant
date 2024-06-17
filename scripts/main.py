import os
import bot
import discord
import platform
import traceback
import get_answer as ga
import update_data as ud

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


if __name__ == "__main__":
    ud.update_data()
    discord_bot = bot.DiscordBot(discord_client)
    discord_client.run(os.getenv("DISCORD_TOKEN"))
    print("Exit")
