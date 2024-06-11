import os
import time
import misc
import discord
import platform

os_name = platform.system()
if os_name == "Linux":
    LOG_CHANNEL_ID = 1244676938002468939
else:
    LOG_CHANNEL_ID = 1248628675134488637
now = time.localtime()


async def send_temp_message(discord_client, message):
    temp_message = await message.reply("잠시 기다려주세요.", mention_author=True)
    await send_log(discord_client, 6, var=(message))

    return temp_message


async def send(
    discord_client,
    msg,
    message,
    ans_json=None,
    image=None,
    log_type=3,
    error=None,
    temp_message=None,
):
    if temp_message != None:
        await temp_message.delete()

    if image == None:
        await message.reply(msg, mention_author=True)
        # await channel.send(msg)
        await send_log(
            discord_client,
            log_type,
            var=(message, ans_json, msg, image, error),
        )

        return

    await message.reply(msg, file=discord.File(image), mention_author=True)
    # await channel.send(msg, file=discord.File(image))
    await send_log(discord_client, log_type, var=(message, ans_json, msg, image, error))
    os.remove(image)


async def send_log(discord_client, log_type, var=None):
    """
    log_type: 1 - 로그인
    log_type: 2 - 로그아웃
    log_type: 3 - 명령어 로그
    log_type: 4 - 관리자 명령어 로그
    log_type: 5 - 에러 로그
    log_type: 6 - 임시 메시지 로그
    """

    if log_type == 1:
        embed = discord.Embed()
        embed.title = "투다이스 어시스턴트 로그인"
        embed.color = discord.Color.green()

        embed_json = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S", now),
            "ip": misc.get_ip(),
            "server_count": str(len(discord_client.guilds)),
            "server_list": "```"
            + ", ".join([guild.name for guild in discord_client.guilds])
            + "```",
            "user_count": str(len(discord_client.users)),
            "user_list": "```"
            + ", ".join([user.name for user in discord_client.users])
            + "```",
        }

        for key, value in embed_json.items():
            if value != None:
                embed.add_field(
                    name=key,
                    value=value,
                    inline=False,
                )

        await discord_client.get_channel(LOG_CHANNEL_ID).send(embed=embed)

    elif log_type == 2:
        embed = discord.Embed()
        embed.title = "투다이스 어시스턴트 로그아웃"
        embed.color = discord.Color.orange()

        embed_json = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S", now),
        }

        for key, value in embed_json.items():
            if value != None:
                embed.add_field(
                    name=key,
                    value=value,
                    inline=False,
                )

        await discord_client.get_channel(LOG_CHANNEL_ID).send(embed=embed)

    elif (log_type == 3) or (log_type == 4):
        message, ans_json, msg, image, error = var
        guild = await discord_client.fetch_guild(message.guild.id)
        member = await guild.fetch_member(message.author.id)
        embed_json = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S", now),
            "server": message.guild.name,
            "channel": message.channel.mention,
            "author": f"{member.display_name} ({message.author.name})",
            "text": message.content,
            "ans_json": ans_json,
            "msg": msg,
        }

        embed = discord.Embed()
        if log_type == 3:
            embed.title = "투다이스 어시스턴트 명령어 로그"
            embed.color = discord.Color.blue()

        elif log_type == 4:
            embed.title = "투다이스 어시스턴트 관리자 명령어 로그"
            embed.color = discord.Color.purple()

        for key, value in embed_json.items():
            if value != None:
                embed.add_field(
                    name=key,
                    value=value,
                    inline=False,
                )

        await discord_client.get_channel(LOG_CHANNEL_ID).send(embed=embed)

        if image == None:
            return

        await discord_client.get_channel(LOG_CHANNEL_ID).send(file=discord.File(image))

    elif log_type == 5:
        message, ans_json, msg, image, error = var
        guild = await discord_client.fetch_guild(message.guild.id)
        member = await guild.fetch_member(message.author.id)
        embed_json = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S", now),
            "server": message.guild.name,
            "channel": message.channel.mention,
            "author": f"{member.display_name} ({message.author.name})",
            "text": message.content,
            "ans_json": ans_json,
            "msg": msg,
            "error": error,
        }

        embed = discord.Embed()
        embed.title = "투다이스 어시스턴트 에러 로그"
        embed.color = discord.Color.red()

        for key, value in embed_json.items():
            if value != None:
                embed.add_field(
                    name=key,
                    value=value,
                    inline=False,
                )

        await discord_client.get_channel(LOG_CHANNEL_ID).send(embed=embed)

    elif log_type == 6:
        message = var
        guild = await discord_client.fetch_guild(message.guild.id)
        member = await guild.fetch_member(message.author.id)
        embed_json = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S", now),
            "server": message.guild.name,
            "channel": message.channel.mention,
            "author": f"{member.display_name} ({message.author.name})",
            "text": message.content,
        }

        embed = discord.Embed()
        embed.title = "투다이스 어시스턴트 임시 메시지 로그"
        embed.color = discord.Color.dark_grey()

        for key, value in embed_json.items():
            if value != None:
                embed.add_field(
                    name=key,
                    value=value,
                    inline=False,
                )

        await discord_client.get_channel(LOG_CHANNEL_ID).send(embed=embed)
