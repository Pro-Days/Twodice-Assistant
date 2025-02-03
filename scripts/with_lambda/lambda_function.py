import json
import os
import traceback

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

import get_rank_info as gri


PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")


def lambda_handler(event, context):
    try:
        print(f"start!\nevent: {event}")

        body = json.loads(event["body"])

        signature = event["headers"]["x-signature-ed25519"]
        timestamp = event["headers"]["x-signature-timestamp"]

        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

        message = timestamp + event["body"]

        print("verify start")
        try:
            verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
        except BadSignatureError:
            return {"statusCode": 401, "body": json.dumps("invalid request signature")}

        print("verify complete")

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
        print("랭킹 command received")
        page = body["data"]["options"][0]["value"] if "options" in body["data"] else 1
        image_data = gri.get_rank_info(page)
        print("랭킹 image generated")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "type": 4,
                    "data": {
                        "content": "랭킹 정보",
                    },
                }
            ),
        }
    else:
        print("unhandled command: " + command)
        return {"statusCode": 400, "body": json.dumps("unhandled command")}


if __name__ == "__main__":
    pass
