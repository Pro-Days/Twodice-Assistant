import os
import bot
import misc
import random
import discord
import platform
import get_answer as ga
import update_data as ud
import cloud_storage as cs
import get_rank_info as gri
import register_player as rp
import get_server_info as gsi
import get_character_info as gci

os_name = platform.system()
if os_name == "Linux":
    LOG_CHANNEL_ID = 1244676938002468939
    ADMIN_CHANNEL_ID = 1244674283826053241
    ADMIN_ID = 407775594714103808
else:
    LOG_CHANNEL_ID = 1248628675134488637
    ADMIN_CHANNEL_ID = 1248627932037910558
    ADMIN_ID = 407775594714103808

print("-" * 20 + "start!")
# nordvpn()

discord_client = discord.Client(intents=discord.Intents.all())

datafile_list = [
    "playerdata.csv",
    "rankdata.csv",
    "registered_player_list.json",
    "serverdata.csv",
]

if os_name == "Linux":
    for datafile in datafile_list:
        cs.download_file(f"data/{datafile}", f"data\\{datafile}")
    ud.update_data()


@discord_client.event
async def on_ready():
    print(f"'{discord_client.user.name}' 로그인 성공 (ID: {discord_client.user.id})")
    await bot.send_log(discord_client, log_type=1, var=None)


@discord_client.event
async def on_message(message):
    if (message.channel.id == ADMIN_CHANNEL_ID) and (message.author.id == ADMIN_ID):
        await admin(message)

    elif message.content.startswith("!한월"):
        ans_json = await ga.get_ans(message, questions)
        try:
            await hanwol(message, ans_json)
        except Exception as e:
            await bot.send(
                discord_client,
                "죄송하지만 오류가 발생했어요\n다시 한번 말씀해주시겠어요?",
                message,
                error=e,
                log_type=5,
            )


async def admin(message):
    msg = message.content

    if msg == "stop":
        await bot.send(discord_client, "종료합니다.", message, log_type=4)
        await bot.send_log(discord_client, log_type=2)
        print("디스코드 로그아웃 시작")
        await discord_client.close()

        return

    elif msg == "ip":
        ip = misc.get_ip()
        await bot.send(discord_client, f"아이피 주소: {ip}", message, log_type=4)

        return

    elif msg == "user_list":
        pl_list = rp.registered_player_list()

        msg = (
            f"등록된 유저 수: {len(pl_list)}\n등록된 유저 목록\n"
            + "```"
            + ", ".join(pl_list)
            + "```"
        )

        await bot.send(discord_client, msg, message, log_type=4)

        return

    elif msg == "server_list":
        pl_list = rp.registered_player_list()

        msg = (
            f"서버 수: {str(len(discord_client.guilds))}\n서버 목록\n"
            + "```"
            + ", ".join([guild.name for guild in discord_client.guilds])
            + "```"
        )

        await bot.send(discord_client, msg, message, log_type=4)

        return

    elif msg == "cmd":
        await bot.send(
            discord_client,
            "1. stop\n2. ip\n3. user_list\n4. server_list\n5. cmd",
            message,
            log_type=4,
        )

        return


async def hanwol(message, ans_json):
    """
    fn_id: -1 - 일반 메시지
    fn_id: 1 - 서버 정보
    fn_id: 2 - 랭킹 정보
    fn_id: 3 - 캐릭터 정보
    fn_id: 4 - 캐릭터 등록
    """

    msg = message.content[4:]
    if ans_json["q"]:
        questions.append(
            {
                "user": message.author.id,
                "msg": f"USER: {msg}\nASSISTANT: {ans_json}",
            },
        )
        await bot.send(discord_client, ans_json["text"], message, ans_json)

        return

    if ans_json["fn_id"] == -1:
        await bot.send(
            discord_client,
            ans_json["text"],
            message,
            ans_json,
        )

        return

    elif ans_json["fn_id"] == 1:
        temp_message = await bot.send_temp_message(discord_client, message)

        info, image = gsi.get_server_info()

        if info != None:
            vote, pl = info

        match info, image:
            case None, None:
                msg = [
                    "죄송하지만 지금은 서버 정보를 가져올 수 없어요.",
                    "죄송해요. 마인리스트와 마인페이지에서 정보를 가져오는데 실패했어요.",
                    "죄송하지만 서버 정보를 가져오는 데 문제가 발생했어요.",
                    "죄송하지만 지금은 마인리스트와 마인페이지에서 정보를 가져올 수 없어요.",
                ]

            case None, _:
                msg = [
                    "마인리스트에 등록되어있는 정보를 보여드릴게요.",
                    "마인리스트에 등록된 정보를 가져왔어요.",
                    "마인리스트에 등록된 정보를 보여드릴게요.",
                    "아래 이미지는 마인리스트에서 가져온 서버 정보에요.",
                ]

            case _, None:
                msg = [
                    f"마인페이지에 따르면 한월 서버의 현재 접속자 수는 {pl}명이고, 추천 수는 {vote}개에요.",
                    f"마인페이지에서 확인된 정보로는 한월 서버의 현재 접속자 수는 {pl}명이고, 추천 수는 {vote}개에요.",
                    f"마인페이지에 따르면 지금 한월 서버의 접속자 수는 {pl}명이고 추천 수는 {vote}개에요.",
                    f"마인리스트가 제공하는 데이터에 따르면 현재 한월 서버의 접속자 수는 {pl}명이고 추천 수는 {vote}개에요.",
                ]

            case _, _:
                msg = [
                    f"마인페이지에 따르면 한월 서버의 현재 접속자 수는 {pl}명이고, 추천 수는 {vote}개에요.\n아래 이미지는 마인리스트에 등록되어있는 정보에요.",
                    f"마인페이지에서 확인된 정보로는 한월 서버의 현재 접속자 수는 {pl}명이고, 추천 수는 {vote}개에요.\n마인페이지에서는 아래 이미지와 같은 정보를 제공하고 있어요.",
                    f"마인페이지에 따르면 지금 한월 서버의 접속자 수는 {pl}명이고 추천 수는 {vote}개에요.\n이 이미지는 마인리스트가 제공하는 정보에요.",
                    f"마인리스트가 제공하는 데이터에 따르면 현재 한월 서버의 접속자 수는 {pl}명이고 추천 수는 {vote}개에요.\n마인리스트는 아래와 같은 정보를 제공하고 있어요.",
                ]

        await bot.send(
            discord_client,
            random.choice(msg),
            message,
            ans_json,
            image=image,
            temp_message=temp_message,
        )

        return

    elif ans_json["fn_id"] == 2:
        temp_message = await bot.send_temp_message(discord_client, message)

        if "page" in ans_json["var"]:
            page = int(ans_json["var"]["page"])
        else:
            page = 1  # 1~
        image = gri.get_rank_info(page)

        if image == None:
            if page != 1:
                msg = [
                    f"죄송하지만 {page}페이지의 랭킹 정보를 불러올 수 없어요.",
                    f"죄송해요. {page}페이지의 랭킹 정보는 알려드릴 수 없어요.",
                    f"죄송하지만 {page}페이지의 랭킹 데이터를 가져올 수 없어요.",
                    f"죄송해요. {page}페이지의 랭킹 정보를 찾을 수 없어요.",
                    f"죄송해요. {page}페이지의 랭킹 정보를 불러오는데 실패했어요.",
                    f"죄송하지만 {page}페이지의 랭킹 정보를 불러오는 데 문제가 발생했어요.",
                ]

            else:
                msg = [
                    "죄송하지만 현재 랭킹 정보를 불러올 수 없어요.",
                    "죄송하지만 지금은 랭킹 데이터를 가져올 수 없어요.",
                    "죄송해요. 랭킹 정보를 불러오는데 실패했어요.",
                    "죄송하지만 랭킹 정보를 불러오는 데 문제가 발생했어요.",
                ]
            await bot.send(
                discord_client,
                random.choice(msg),
                message,
                ans_json,
                temp_message=temp_message,
            )

            return

        if page == 1:
            msg = [
                f"한월 서버의 캐릭터 레벨 랭킹을 보여드릴게요.",
                f"한월 서버의 캐릭터 랭킹을 알려드릴게요.",
                f"지금 한월 서버의 캐릭터 랭킹은 다음과 같아요.",
                f"한월 서버의 레벨 순위를 보여드릴게요.",
                f"지금 한월의 레벨 랭킹을 보여드릴게요.",
            ]

        else:
            msg = [
                f"한월 서버의 {page}페이지 캐릭터 레벨 랭킹을 보여드릴게요.",
                f"한월 서버의 {page}페이지 레벨 랭킹을 알려드릴게요.",
                f"이 이미지는 지금 한월 서버의 {page}페이지 캐릭터 랭킹이에요.",
                f"아래 이미지는 한월 서버의 {page}페이지 캐릭터 순위에요.",
                f"지금 한월의 {page}페이지 레벨 랭킹을 보여드릴게요.",
            ]

        await bot.send(
            discord_client,
            random.choice(msg),
            message,
            ans_json,
            image=image,
            temp_message=temp_message,
        )

        return

    elif ans_json["fn_id"] == 3:
        temp_message = await bot.send_temp_message(discord_client, message)

        name = ans_json["var"]["name"]
        if "slot" in ans_json["var"]:
            slot = ans_json["var"]["slot"]
            default = False

        else:
            slot = 1  # 1~3
            default = True

        period = ans_json["var"]["period"] if "period" in ans_json["var"] else 7

        if not rp.is_registered(name):
            """셀레니움으로 크롤링해서 현재 캐릭터 정보 가져오기"""
            msg = [
                "그 플레이어는 등록되지 않았어요.",
                "해당 플레이어는 등록되어 있지 않아요.",
                "말씀하신 플레이어는 등록되지 않았어요.",
                "해당 플레이어는 목록에 등록되어 있지 않아요.",
                "찾으시는 플레이어는 등록되지 않았어요.",
            ]
            await bot.send(
                discord_client,
                random.choice(msg),
                message,
                ans_json,
                temp_message=temp_message,
            )

            return

        msg, image = gci.get_character_info(name, slot, period=period, default=default)
        await bot.send(
            discord_client,
            msg,
            message,
            ans_json,
            image=image,
            temp_message=temp_message,
        )

        return

    elif ans_json["fn_id"] == 4:
        temp_message = await bot.send_temp_message(discord_client, message)

        name = ans_json["var"]["name"]

        if "slot" in ans_json["var"]:
            slot = int(ans_json["var"]["slot"])

        else:
            slot = 1

        rp.register_player(name, slot)

        name = misc.get_real_name(name)
        msg = [
            f"{name} 캐릭터를 메인 슬롯 {slot}번으로 등록했어요!",
            f"{name} 등록 완료! 메인 슬롯은 {slot}번으로 설정했어요.",
            f"메인슬롯 {slot}번으로 {name} 캐릭터 등록에 성공했어요.",
        ]
        msg = random.choice(msg)

        if msg.count("_") >= 2:
            msg += "\n실제로는 언더바(_)가 정상적으로 적용되니 걱정마세요!"

        await bot.send(
            discord_client, msg, message, ans_json, temp_message=temp_message
        )

        return


if __name__ == "__main__":
    questions = []

    discord_client.run(os.getenv("DISCORD_TOKEN"))

    print(f"디스코드 로그아웃 성공")
    # disconnect_nordvpn()

    if os_name == "Linux":
        print("파일 업로드 시작")
        for datafile in datafile_list:
            cs.upload_file(f"data\\{datafile}", f"data/{datafile}")
        print("파일 업로드 완료")
    print("종료 - Ip: " + misc.get_ip())
