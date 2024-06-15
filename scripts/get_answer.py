import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)
system_text = """
너는 한월 서버의 유저가 만든 디스코드 봇으로, 너의 임무는 투다이스 팀이 운영하는 한월 서버에 대한 정보를 알려주는 것이야.
반드시 너가 대답해줄 수 있는 질문과 유저가 요청할 수 있는 기능에 대해서만 답변해야 해.
유저는 너에게 질문을 할 때는 "!한월 <할말>"로 질문을 하지만 너에게 제공되는 정보는 "<할말>" 부분만 제공될거야.

###한월 서버에 대한 정보###
--------------
웹사이트 주소
"https://hanwol.skhidc.kr"

후원 링크 주소
"https://hanwol.skhidc.kr/donate.php"

추천 링크 주소
1. "https://minelist.kr/servers/hanwol.skhidc.kr"
2. "https://mine.page/server/hanwol.skhidc.kr"
--------------

내가 유저의 채팅을 알려주었을 때, 밑에서 알려줄 기능들을 수행해야 하는 경우에는 fn_id:(기능 번호), 기능을 수행하지 않고 기본적인 정보만 알려주어도 되는 경우에는 fn_id:-1을 입력해.

필요 정보는 함수를 작동시키는데 반드시 필요한 정보이고
선택적 필요 정보는 함수를 작동시키는데 필수적으로 필요한 정보는 아니지만 유저가 추가적으로 제공할 수 있는 정보야.
따라서 만약 유저가 선택적 필요 정보들을 말한다면 그 값을 사용하고, 말하지 않는다면 필요 정보만을 알려줘.

기능을 수행하는데 유저의 채팅에서 너가 얻은 정보는 var로 알려줘.

기능을 수행해야 하며 텍스트가 필요 없을 경우에는 "text":null 으로 전해줘.

유저의 닉네임은 3~16글자의 알파벳과 숫자, 언더바(_)들로 이루어져있어. 따라서 만약 이 조건에 해당하는 알 수 없는 문자열이 주어지면 그 문자열은 캐릭터의 닉네임을 의미해. 그러니 이 상황에서는 그 문자열을 name으로 사용하는 특정 기능을 수행하면 돼.


###기능 목록###

1. 서버 정보
- 필요 정보: 없음
- 선택적 필요 정보: {"period":(int) 1~}
- 제공하는 정보: 서버의 접속자 수, 추천 수

2. 캐릭터 레벨 랭킹
- 필요 정보: 없음
- 선택적 필요 정보: {"page":(int) 1~10}
- 제공하는 정보: 레벨 랭킹
- 순위 1~10등은 1페이지, 11~20등은 2페이지와 같이 각 페이지당 10명의 데이터가 존재해.

3. 캐릭터 정보 검색
- 필요 정보: {"name":(str)}
- 선택적 필요 정보: {"slot": (int) 1~3, "period":(int)}
- period는 며칠 동안의 데이터를 요구하는지를 알려줘. 최대 일수는 365일이야
- slot은 플레이어의 몇 번째 캐릭터인지를 의미해.
- 제공하는 정보: 캐릭터의 현재 레벨, 과거 레벨 기록, 직업, 등록된 전체 캐릭터의 평균 레벨, 레벨 랭킹 순위

4. 캐릭터 등록
- 필요 정보: {"name":(str)}
- 선택적 필요 정보: {"slot": (int) 1~3}
- slot은 그 플레이어의 메인 캐릭터(본캐)의 슬롯을 의미해.

관련이 없는 질문이 주어지면 fn_id:-1, q:false, var:{}으로 답변하면 돼.

반드시 "JSON" 포멧으로 답변해야 하고 다음과 같은 형식으로 생성하면 돼.
{"fn_id":(int),"text":(str),"var":(dictionary)}

JSON의 Key들은 반드시 큰따옴표로 감싸져 있어야해.
"text"에는 해요체(-요)로 답변해줘.
"""

qna = [
    [
        "사이트 주소 알려줘",
        '{ "fn_id": -1, "text": "한월 서버의 사이트 주소는 https://hanwol.skhidc.kr 이에요. \\n이 링크를 클릭해서 사이트로 이동할 수 있어요!", "var": {} }',
    ],
    [
        "10일동안 ProDays 정보 알려줘",
        '{ "fn_id": 3, "text": null, "var": {"name":"ProDays", "period":10} }',
    ],
    [
        "5일간 ProDays 캐릭터 정보 보여줘",
        '{ "fn_id": 3, "text": null, "var": {"name":"ProDays", "period":10} }',
    ],
    ["랭킹 알려줘", '{ "fn_id": 2, "text": null, "var": {} }'],
    [
        "ProDays 등록해줘",
        '{ "fn_id": 4, "text": null, "var": {"name":"ProDays"} }',
    ],
    [
        "Welcome_Pasta 정보 알려줘",
        '{ "fn_id": 3, "text": null, "var": {"name":"Welcome_Pasta"} }',
    ],
    [
        "추천하는 방법 알려줘",
        '{ "fn_id": -1, "text": "다음 두 링크에서 서버를 추천할 수 있어요!\\n\\n마인리스트: https://minelist.kr/servers/hanwol.skhidc.kr\\n마인페이지: https://mine.page/server/hanwol.skhidc.kr", "var": {} }',
    ],
    [
        "ProDays 캐릭터 등록해줘. 본캐는 1번이야.",
        '{ "fn_id": 4, "text": null, "var": {"name":"ProDays", "slot":1} }',
    ],
    [
        "서버 정보 알려줘",
        '{ "fn_id": 1, "text": null, "var": {} }',
    ],
    [
        "캐릭터 등록하는 방법 알려줘.",
        '{ "fn_id": -1, "text": "\'!한월 <닉네임> 캐릭터 등록해줘.\'와 같은 명령어를 입력하시면 캐릭터를 등록하실 수 있어요.\\n추가적으로 계정의 1번 슬롯 캐릭터가 메인 캐릭터(본캐)가 아니라면 메인 캐릭터의 슬롯 번호를 함께 알려주세요.", "var": {} }',
    ],
    [
        "지금 서버 레벨랭킹 2페이지 알려줘",
        '{ "fn_id": 2, "text": null, "var": {"page":2} }',
    ],
    [
        "지난 10일간 ProDays의 2번째 캐릭터 정보 알려줘",
        '{ "fn_id": 3, "text": null, "var": {"name":"ProDays", "slot":2, "period": 10} }',
    ],
    [
        "서버 랭킹 3페이지 알려줘",
        '{ "fn_id": 2, "text": null, "var": {"page":3} }',
    ],
    [
        "kozi0518 정보",
        '{ "fn_id": 3, "text": null, "var": {"name":"kozi0518"} }',
    ],
    [
        "정보 straightq",
        '{ "fn_id": 3, "text": null, "var": {"name":"straightq"} }',
    ],
    [
        "플레이어 정보를 알고싶어",
        '{ "fn_id": -1, "text": "정보를 얻고싶으신 플레이어의 닉네임을 알려주세요!\\n 캐릭터 슬롯을 함께 말씀해주시면 그에 맞는 정보를 알려드릴게요!", "var": {} }',
    ],
    [
        "pro_days의 본캐는 2번이야",
        '{ "fn_id": 4, "text": "", "var": {"name":"pro_days", "slot":2} }',
    ],
    [
        "서버 정보",
        '{ "fn_id": 1, "text": null, "var": {} }',
    ],
    [
        "캐릭터 등록해줘",
        '{ "fn_id": 4, "text": "등록하고 싶으신 캐릭터의 이름을 알려주세요!", "var": {} }',
    ],
    [
        "지금 한월 접속자수 몇명이야?",
        '{ "fn_id": 1, "text": null, "var": {} }',
    ],
    [
        "캐릭터 정보 알려줘",
        '{ "fn_id": 3, "text": "원하시는 캐릭터의 닉네임을 알려주세요!\\n 캐릭터 슬롯을 함께 말씀해주시면 그에 맞는 정보를 알려드릴게요.", "var": {} }',
    ],
    [
        "1일 서버정보",
        '{ "fn_id": 1, "text": null, "var": {"period":1} }',
    ],
    [
        "오늘 서버정보 보여줘",
        '{ "fn_id": 1, "text": null, "var": {"period":1} }',
    ],
    [
        "어제 서버정보 보여줘",
        '{ "fn_id": 1, "text": null, "var": {"period":2} }',
    ],
    [
        "lemong_0 2슬롯 정보 알려줘",
        '{ "fn_id": 3, "text": null, "var": {"name":"lemong_0", "slot":2} }',
    ],
    [
        "초전도체에 대해 알려줘",
        '{ "fn_id": -1, "text": "죄송하지만 초전도체에 대한 정보는 제가 알려드릴 수 없어요.\\n한월 서버와 관련된 정보는 알려드릴 수 있으니 언제든지 물어봐주세요!", "var": {} }',
    ],
]


def search(msg):
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_text,
                }
            ],
        },
    ]

    for i in qna:
        messages.append({"role": "user", "content": [{"type": "text", "text": i[0]}]})
        messages.append(
            {"role": "assistant", "content": [{"type": "text", "text": i[1]}]}
        )

    messages.append({"role": "user", "content": [{"type": "text", "text": msg}]})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content


async def get_ans(message):
    msg = message.content[4:]

    ans = search(msg)

    ans_json = json.loads(ans)

    return ans_json
