import json
import os
import traceback

import misc
import get_rank_info as gri
import send_msg as sm
import register_player as rp


PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")
LOG_CHANNEL_ID = os.getenv("DISCORD_LOG_CHANNEL_ID")
ADMIN_CHANNEL_ID = os.getenv("DISCORD_ADMIN_CHANNEL_ID")
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

    if (body["channel_id"] == ADMIN_CHANNEL_ID) and (body["member"]["user"]["id"] == ADMIN_ID):
        admin(event, cmd)

    elif cmd == "랭킹":
        print("랭킹 command received")
        page = body["data"]["options"][0]["value"] if "options" in body["data"] else 1
        image_path = gri.get_rank_info(page)
        print("랭킹 image generated")

        if page == 1:
            msg = "지금 한월 RPG의 캐릭터 랭킹을 보여드릴게요."
        else:
            msg = f"지금 한월 RPG의 캐릭터 랭킹 {page}페이지를 보여드릴게요."

        return sm.send(event, msg, image=image_path)
    else:
        print("unhandled command: " + cmd)
        return {"statusCode": 400, "body": json.dumps("unhandled command")}


def admin(event, cmd):

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
