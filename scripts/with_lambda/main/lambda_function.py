import os
import json
import traceback

import misc
import send_msg as sm
import get_rank_info as gri
import register_player as rp
import get_character_info as gci


ADMIN_ID = os.getenv("DISCORD_ADMIN_ID")


def lambda_handler(event, context):
    try:
        print(f"start!\nevent: {event}")
        return command_handler(event)

    except:
        sm.send(event, "오류가 발생했습니다.", log_type=3, error=traceback.format_exc())
        return {"statusCode": 400, "body": json.dumps(traceback.format_exc())}


def command_handler(event):

    body = json.loads(event["body"])
    cmd = body["data"]["name"]

    # 어드민 커맨드
    if body["member"]["user"]["id"] == ADMIN_ID:
        if cmd == "ip":
            ip = misc.get_ip()

            return sm.send(event, f"아이피 주소: {ip}", log_type=2)

        elif cmd == "user_count":
            pl_list = rp.get_registered_players()

            return sm.send(event, f"등록된 유저 수: {len(pl_list)}", log_type=2)

        elif cmd == "server_list":
            server_list = misc.get_guild_list()

            msg = (
                f"서버 수: {len(server_list)}\n서버 목록\n"
                + "```"
                + ", ".join([server["name"] for server in server_list])
                + "```"
            )

            return sm.send(event, msg, log_type=2)

    # 일반 커맨드
    if cmd == "랭킹":
        print("랭킹 command received")

        page = 1
        if "options" in body["data"]:
            for i in body["data"]["options"]:
                if i["name"] == "페이지":
                    page = i["value"]
                    break

        image_path = gri.get_rank_info(page)
        print("랭킹 image generated")

        if page == 1:
            msg = "지금 한월 RPG의 캐릭터 랭킹을 보여드릴게요."
        else:
            msg = f"지금 한월 RPG의 캐릭터 랭킹 {page}페이지를 보여드릴게요."

        return sm.send(event, msg, image=image_path)

    elif cmd == "검색":
        print("검색 command received")

        slot = None
        period = 7
        if "options" in body["data"]:
            for i in body["data"]["options"]:

                if i["name"] == "닉네임":
                    name = i["value"]

                elif i["name"] == "슬롯":
                    slot = i["value"]

                elif i["name"] == "기간":
                    period = i["value"]

        if slot is None:
            slot = misc.get_main_slot(name)
            default = True
        else:
            default = False

        msg, image_path = gci.get_character_info(name, slot, period, default)
        print("검색 image generated")

        return sm.send(event, msg, image=image_path)

    elif cmd == "등록":
        print("등록 command received")

        slot = 1
        if "options" in body["data"]:
            for i in body["data"]["options"]:

                if i["name"] == "닉네임":
                    name = i["value"]

                elif i["name"] == "슬롯":
                    slot = i["value"]

        result = rp.register_player(name, slot)

        if result:
            msg = f"{name}님을 등록했습니다."
        else:
            msg = f"{name}님의 등록에 실패했습니다."

        return sm.send(event, msg)

    else:
        print("unhandled command: " + cmd)
        sm.send(event, "오류가 발생했습니다.", log_type=3, error=f"unhandled command: {cmd}")
        return {"statusCode": 400, "body": json.dumps("unhandled command")}
