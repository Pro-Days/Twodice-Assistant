import json
import os
import traceback
import platform
import random

import get_rank_info as gri
import send_msg as sm


os_name = platform.system()
PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")

if os_name == "Linux":  # Twodice Assistant
    LOG_CHANNEL_ID = 1244676938002468939
    ADMIN_CHANNEL_ID = 1244674283826053241
    ADMIN_ID = 407775594714103808
else:  # TA_DEV
    LOG_CHANNEL_ID = 1248628675134488637
    ADMIN_CHANNEL_ID = 1248628536311550045
    ADMIN_ID = 407775594714103808


def lambda_handler(event, context):
    try:
        print(f"start!\nevent: {event}")
        return command_handler(event)

    except:
        sm.send(event, traceback.format_exc(), log_type=3)
        return {"statusCode": 400, "body": json.dumps(traceback.format_exc())}


def command_handler(event):

    body = json.loads(event["body"])
    cmd = body["data"]["name"]

    if (body["channel_id"] == ADMIN_CHANNEL_ID) and (body["member"]["user"]["id"] == ADMIN_ID):
        # admin(cmd)
        pass

    elif cmd == "랭킹":
        print("랭킹 command received")
        page = body["data"]["options"][0]["value"] if "options" in body["data"] else 1
        image_path = gri.get_rank_info(page)
        print("랭킹 image generated")

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

        return sm.send(event, random.choice(msg), image=image_path)
    else:
        print("unhandled command: " + cmd)
        return {"statusCode": 400, "body": json.dumps("unhandled command")}


# def admin(self, cmd):

#     if cmd == "ip":
#         ip = misc.get_ip()
#         sm.send(f"아이피 주소: {ip}", log_type=2)

#         return

#     elif cmd == "user_list":
#         pl_list = rp.registered_player_list()

#         cmd = f"등록된 유저 수: {len(pl_list)}\n등록된 유저 목록\n" + "```" + ", ".join(pl_list) + "```"

#         self.send(cmd, message, log_type=4)

#         return

#     elif cmd == "server_list":
#         pl_list = rp.registered_player_list()

#         cmd = (
#             f"서버 수: {str(len(self.discord_client.guilds))}\n서버 목록\n"
#             + "```"
#             + ", ".join([guild.name for guild in self.discord_client.guilds])
#             + "```"
#         )

#         self.send(cmd, message, log_type=4)

#         return

#     elif cmd == "cmd":
#         self.send(
#             "1. stop\n2. ip\n3. user_list\n4. server_list\n5. cmd",
#             message,
#             log_type=4,
#         )

#         return
