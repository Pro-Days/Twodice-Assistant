import json
import os
import traceback
from pprint import pprint

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")


def lambda_handler(event, context):
    try:
        pprint("start!\nevent: " + event)

        body = json.loads(event["body"])

        signature = event["headers"]["x-signature-ed25519"]
        timestamp = event["headers"]["x-signature-timestamp"]

        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

        message = timestamp + event["body"]

        pprint("verify start")
        try:
            verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
        except BadSignatureError:
            return {"statusCode": 401, "body": json.dumps("invalid request signature")}

        pprint("verify complete")

        cmd_type = body["type"]

        if cmd_type == 1:
            return {"statusCode": 200, "body": json.dumps({"type": 1})}
        elif cmd_type == 2:
            return command_handler(body)
        else:
            return {"statusCode": 400, "body": json.dumps("unhandled request type")}

    except Exception:
        return {"statusCode": 400, "body": json.dumps(traceback.format_exc())}


def command_handler(body):
    command = body["data"]["name"]

    if command == "랭킹":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "type": 4,
                    "data": {
                        "content": "Hello, World.",
                    },
                }
            ),
        }
    else:
        pprint("unhandled command: " + command)
        return {"statusCode": 400, "body": json.dumps("unhandled command")}


{
    "name": "랭킹",
    "description": "캐릭터 레벨 랭킹을 보여줍니다.",
    "options": [{"name": "페이지", "description": "페이지 번호 (1~10)", "type": 4}],
    "type": 1,
}
{
    "name": "검색",
    "type": 1,
    "description": "캐릭터의 정보를 보여줍니다.",
    "options": [
        {
            "name": "닉네임",
            "description": "캐릭터 닉네임",
            "type": 3,
            "required": True,
        },
        {
            "name": "슬롯",
            "description": "캐릭터 슬롯 번호 (1~5)",
            "type": 4,
            "required": False,
        },
        {
            "name": "기간",
            "description": "캐릭터 정보를 조회할 기간 (1~365)",
            "type": 4,
            "required": False,
        },
    ],
}
{
    "name": "등록",
    "type": 1,
    "description": "일일 정보를 저장하는 캐릭터 목록에 캐릭터를 추가합니다. 과거 시점의 캐릭터 정보 검색을 이용할 수 있게됩니다.",
    "options": [
        {
            "name": "닉네임",
            "description": "캐릭터 닉네임",
            "type": 3,
            "required": True,
        },
        {
            "name": "슬롯",
            "description": "메인 캐릭터 (본캐) 슬롯 번호 (1~5)",
            "type": 4,
            "required": False,
        },
    ],
}
