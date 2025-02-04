import os
import json
import boto3
import traceback

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


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

            lambda_service = boto3.client(service_name="lambda", region_name="ap-northeast-2")
            functionName = "TA_DEV-lambda_main"
            lambda_service.invoke(
                FunctionName=functionName, InvocationType="Event", Payload=json.dumps(event)
            )

            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps(
                    {
                        "type": 5,
                        "data": {"content": "잠시 기다려주세요", "flags": 64},
                    }
                ),
            }
        else:
            return {"statusCode": 400, "body": json.dumps("unhandled request type")}

    except Exception:
        return {"statusCode": 400, "body": json.dumps(traceback.format_exc())}
