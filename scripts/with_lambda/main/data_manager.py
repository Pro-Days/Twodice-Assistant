import os
import boto3
import platform
from boto3.dynamodb.conditions import Key


os_name = platform.system()
if os_name == "Linux":
    session = boto3.Session(
        region_name="ap-northeast-2",
    )
else:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="ap-northeast-2",
    )
dynamodb = session.resource("dynamodb")


def read_data(table_name, index=None, **kwargs):
    table = dynamodb.Table(table_name)

    # value가 범위인 경우 추가 (예: level)
    condition = None
    if kwargs:
        for key, value in kwargs.items():
            if condition is None:
                condition = Key(key).eq(value)
            else:
                condition = condition & Key(key).eq(value)

    if index:
        response = table.query(IndexName=index, KeyConditionExpression=(condition))
    else:
        response = table.query(KeyConditionExpression=(condition))

    items = response.get("Items", [])

    return items if items else None


def scan_data(table_name, key=None):
    table = dynamodb.Table(table_name)

    if key:
        response = table.scan(ProjectionExpression=key)
    else:
        response = table.scan()

    items = response.get("Items", [])

    # 페이지네이션 처리: LastEvaluatedKey가 있으면 계속해서 스캔
    while "LastEvaluatedKey" in response:
        response = table.scan(ProjectionExpression="id", ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    return items if items else None


def write_data(table_name, item):
    table = dynamodb.Table(table_name)

    table.put_item(Item=item)


if __name__ == "__main__":
    # print(scan_data("TA_DEV-Users", "name"))
    pass
