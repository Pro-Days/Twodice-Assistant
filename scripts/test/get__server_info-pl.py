import json
import requests
import time


def hanwol(ans):
    ans_json = json.loads(ans)
    st = time.time()

    if ans_json["fn_id"] == 1:
        online, pl = get_server_info()

        print(f"online: {online}, pl: {pl}")
        print(f"elapsed time: {time.time() - st:.2f}s")


def get_server_info():

    url = "https://mcapi.us/server/status?ip=hanwol.skhidc.kr"
    response = requests.get(url)
    server_data = response.json()

    online = server_data["online"]
    if online:
        pl = server_data["players"]["now"]
    else:
        pl = None

    return online, pl


if __name__ == "__main__":
    hanwol('{ "fn_id": 1, "q": false, "text": null, "var": {} }')
