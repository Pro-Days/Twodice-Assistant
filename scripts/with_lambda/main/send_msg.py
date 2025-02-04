import os
import json
import misc
import requests
import platform
import datetime
from pytz import timezone

LOG_CHANNEL_ID = os.getenv("DISCORD_LOG_CHANNEL_ID")
ADMIN_CHANNEL_ID = os.getenv("DISCORD_ADMIN_CHANNEL_ID")
ADMIN_ID = os.getenv("DISCORD_ADMIN_ID")


# def hanwol(self, message, ans_json):
#     """
#     fn_id: -1 - 일반 메시지
#     fn_id: 1 - 서버 정보
#     fn_id: 2 - 랭킹 정보
#     fn_id: 3 - 캐릭터 정보
#     fn_id: 4 - 캐릭터 등록
#     """

#     msg = message.content[4:]

#     if ans_json["fn_id"] == -1:
#         await self.send(
#             ans_json["text"],
#             message,
#             ans_json,
#         )

#         return

#     elif ans_json["fn_id"] == 1:
#         temp_message = await self.send_temp_message(message)

#         period = ans_json["var"]["period"] if "period" in ans_json["var"] else 7

#         msg, image = gsi.get_server_info(period)

#         await self.send(
#             msg,
#             message,
#             ans_json,
#             image=image,
#             temp_message=temp_message,
#         )

#         return

#     elif ans_json["fn_id"] == 2:
#         temp_message = await self.send_temp_message(message)

#         if "page" in ans_json["var"]:
#             page = int(ans_json["var"]["page"])
#         else:
#             page = 1  # 1~
#         image = gri.get_rank_info(page)

#         if image == None:
#             if page != 1:
#                 msg = [
#                     f"죄송하지만 {page}페이지의 랭킹 정보를 불러올 수 없어요.",
#                     f"죄송해요. {page}페이지의 랭킹 정보는 알려드릴 수 없어요.",
#                     f"죄송하지만 {page}페이지의 랭킹 데이터를 가져올 수 없어요.",
#                     f"죄송해요. {page}페이지의 랭킹 정보를 찾을 수 없어요.",
#                     f"죄송해요. {page}페이지의 랭킹 정보를 불러오는데 실패했어요.",
#                     f"죄송하지만 {page}페이지의 랭킹 정보를 불러오는 데 문제가 발생했어요.",
#                 ]

#             else:
#                 msg = [
#                     "죄송하지만 현재 랭킹 정보를 불러올 수 없어요.",
#                     "죄송하지만 지금은 랭킹 데이터를 가져올 수 없어요.",
#                     "죄송해요. 랭킹 정보를 불러오는데 실패했어요.",
#                     "죄송하지만 랭킹 정보를 불러오는 데 문제가 발생했어요.",
#                 ]
#             await self.send(
#                 random.choice(msg),
#                 message,
#                 ans_json,
#                 temp_message=temp_message,
#             )

#             return

#         if page == 1:
#             msg = [
#                 f"한월 서버의 캐릭터 레벨 랭킹을 보여드릴게요.",
#                 f"한월 서버의 캐릭터 랭킹을 알려드릴게요.",
#                 f"지금 한월 서버의 캐릭터 랭킹은 다음과 같아요.",
#                 f"한월 서버의 레벨 순위를 보여드릴게요.",
#                 f"지금 한월의 레벨 랭킹을 보여드릴게요.",
#             ]

#         else:
#             msg = [
#                 f"한월 서버의 {page}페이지 캐릭터 레벨 랭킹을 보여드릴게요.",
#                 f"한월 서버의 {page}페이지 레벨 랭킹을 알려드릴게요.",
#                 f"이 이미지는 지금 한월 서버의 {page}페이지 캐릭터 랭킹이에요.",
#                 f"아래 이미지는 한월 서버의 {page}페이지 캐릭터 순위에요.",
#                 f"지금 한월의 {page}페이지 레벨 랭킹을 보여드릴게요.",
#             ]

#         await self.send(
#             random.choice(msg),
#             message,
#             ans_json,
#             image=image,
#             temp_message=temp_message,
#         )

#         return

#     elif ans_json["fn_id"] == 3:
#         temp_message = await self.send_temp_message(message)

#         name = ans_json["var"]["name"]
#         if "slot" in ans_json["var"]:
#             slot = ans_json["var"]["slot"]
#             default = False

#         else:
#             slot = rp.get_main_slot(name)  # 1~3
#             default = True

#         period = ans_json["var"]["period"] if "period" in ans_json["var"] else 7

#         if not rp.is_registered(name):
#             """셀레니움으로 크롤링해서 현재 캐릭터 정보 가져오기"""
#             msg = [
#                 "그 플레이어는 등록되지 않았어요.",
#                 "해당 플레이어는 등록되어 있지 않아요.",
#                 "말씀하신 플레이어는 등록되지 않았어요.",
#                 "해당 플레이어는 목록에 등록되어 있지 않아요.",
#                 "찾으시는 플레이어는 등록되지 않았어요.",
#             ]
#             await self.send(
#                 random.choice(msg),
#                 message,
#                 ans_json,
#                 temp_message=temp_message,
#             )

#             return

#         msg, image = gci.get_character_info(name, slot, period=period, default=default)
#         await self.send(
#             msg,
#             message,
#             ans_json,
#             image=image,
#             temp_message=temp_message,
#         )

#         return

#     elif ans_json["fn_id"] == 4:
#         temp_message = await self.send_temp_message(message)

#         name = ans_json["var"]["name"]

#         if "slot" in ans_json["var"]:
#             slot = int(ans_json["var"]["slot"])

#         else:
#             slot = 1

#         rp.register_player(name, slot)

#         name = misc.get_real_name(name)
#         msg = [
#             f"{name} 캐릭터를 메인 슬롯 {slot}번으로 등록했어요!",
#             f"{name} 등록 완료! 메인 슬롯은 {slot}번으로 설정했어요.",
#             f"메인슬롯 {slot}번으로 {name} 캐릭터 등록에 성공했어요.",
#         ]
#         msg = random.choice(msg)

#         if msg.count("_") >= 2:
#             msg += "\n실제로는 언더바(_)가 정상적으로 적용되니 걱정마세요!"

#         await self.send(msg, message, ans_json, temp_message=temp_message)

#         return


def send(event, msg, image=None, log_type=1, error=None):
    body = json.loads(event["body"])
    interaction_token = body.get("token")

    payload = {"content": msg}

    if image:
        with open(image, "rb") as f:
            file_data = f.read()

        url = f"https://discord.com/api/v10/webhooks/{os.getenv('DISCORD_APP_ID')}/{interaction_token}"
        multipart_data = {
            "payload_json": (None, json.dumps(payload), "application/json"),
            "file": (image, file_data, "application/octet-stream"),
        }

        response = requests.post(url, files=multipart_data)

        print(f"메시지 전송 완료: {response.json()}, {msg}")

        send_log(log_type, event, msg if error == None else error, image)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "메시지 전송 성공", "response": response.json(), "msg": msg}),
        }

    else:
        url = f"https://discord.com/api/v10/webhooks/{os.getenv("DISCORD_APP_ID")}/{interaction_token}/messages/@original"

        headers = {"Content-Type": "application/json"}

        response = requests.patch(url, headers=headers, data=json.dumps(payload))

        print(f"메시지 전송 완료: {response.json()}, {msg}")

        send_log(log_type, event, msg if error == None else error)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "메시지 전송 성공", "response": response.json(), "msg": msg}),
        }


def send_log(log_type, event, msg, image=None):
    """
    log_type: 1 - 명령어 로그
    log_type: 2 - 관리자 명령어 로그
    log_type: 3 - 에러 로그
    """

    body = json.loads(event["body"])

    guild_id = body["guild_id"]
    guild_name = misc.get_guild_name(guild_id)
    channel_id = body["channel"]["id"]
    channel_name = body["channel"]["name"]
    member_id = body["member"]["user"]["id"]
    member_name = body["member"]["user"]["global_name"]
    member_username = body["member"]["user"]["username"]

    if (log_type == 1) or (log_type == 2):

        embed_json = {
            "time": datetime.datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S"),
            "server": f"{guild_name} ({guild_id})",
            "channel": f"{channel_name} ({channel_id})",
            "author": f"{member_username} - {member_name} ({member_id})",
            "cmd": (
                f"{body["data"]["name"]}\n{', '.join([f"{option['name']}: {option['value']}" for option in body['data']['options']])}"
                if "options" in body["data"]
                else body["data"]["name"]
            ),
            "msg": msg,
        }

        if log_type == 1:
            title = "투다이스 어시스턴트 명령어 로그"
            color = 3447003

        elif log_type == 2:
            title = "투다이스 어시스턴트 관리자 명령어 로그"
            color = 10181046

        fields = []
        for key, value in embed_json.items():
            if value != None:
                fields.append(
                    {
                        "name": key,
                        "value": value,
                        "inline": False,
                    }
                )

    elif log_type == 3:
        embed_json = {
            "time": datetime.datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S"),
            "server": f"{guild_name} ({guild_id})",
            "channel": f"{channel_name} ({channel_id})",
            "author": f"{member_username} - {member_name} ({member_id})",
            "cmd": (
                f"{body["data"]["name"]}\n{', '.join([f"{option['name']}: {option['value']}" for option in body['data']['options']])}"
                if "options" in body["data"]
                else body["data"]["name"]
            ),
            "error": msg,
        }

        title = "투다이스 어시스턴트 명령어 에러 로그"
        description = f"<@{ADMIN_ID}>"
        color = 15548997

        fields = []
        for key, value in embed_json.items():
            if value != None:
                fields.append(
                    {
                        "name": key,
                        "value": value,
                        "inline": False,
                    }
                )

    # 로그 전송
    payload = (
        {"content": "Content", "embeds": [{"title": title, "color": color, "fields": fields}]}
        if log_type != 3
        else {
            "content": "Content",
            "embeds": [{"title": title, "description": description, "color": color, "fields": fields}],
        }
    )

    url = f"https://discord.com/api/v10/channels/{LOG_CHANNEL_ID}/messages"

    headers = {"Authorization": f"Bot {os.getenv('DISCORD_TOKEN')}", "Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print(f"로그 전송 완료: {response.json()}, {msg}")

    # 이미지 전송
    if image:
        with open(image, "rb") as f:
            file_data = f.read()

        payload = {
            "content": "",
        }
        headers = {"Authorization": f"Bot {os.getenv('DISCORD_TOKEN')}", "Content-Type": "application/json"}

        url = f"https://discord.com/api/v10/channels/{LOG_CHANNEL_ID}/messages"

        multipart_data = {
            "payload_json": (None, json.dumps(payload), "application/json"),
            "file": (image, file_data, "application/octet-stream"),
        }

        response = requests.post(url, headers=headers, files=multipart_data)

    print(f"로그 전송 완료: {response.json()}, {msg}")
