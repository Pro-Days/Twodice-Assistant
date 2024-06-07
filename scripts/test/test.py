import random


def shift_elements_randomly(elements):
    length = len(elements)
    new_list = [None] * length  # 새로운 리스트를 None으로 초기화
    positions_filled = [False] * length  # 각 위치가 채워졌는지 추적

    for i in range(length):
        while True:
            shift = random.randint(-2, 2)  # -2부터 2까지의 랜덤 정수 생성
            new_position = (i + shift) % length
            if not positions_filled[new_position]:  # 해당 위치가 비어있는 경우에만 이동
                new_list[new_position] = elements[i]
                positions_filled[new_position] = True
                break

    return new_list


# 원래 문자열 리스트
original_list = [
    "ProDays",
    "neoreow",
    "Aventurine_0",
    "ino2423",
    "ljinsoo",
    "krosh0127",
    "heekp",
    "Seyene",
    "Route88",
    "Lemong_0",
    "_IIN",
    "ggameee",
    "YOUKONG",
    "sungchanmom",
    "xunzeeya",
    "Master_Rakan_",
    "Moncler02",
    "tmdwns0818",
    "roadhyeon03",
    "aaqq2005y",
    "spemdnjs",
    "imsouthkorean",
    "world_3034",
    "poro_rany",
    "Welcome_Pasta",
    "d_capo",
    "LGJ20000",
    "TinySlayers",
    "ArtBeat",
    "TuuNaaA1",
]

# 무작위로 이동한 리스트
shifted_randomly = shift_elements_randomly(original_list)

# 결과 출력
print("Original list:")
print(", ".join(original_list))
print("\nShifted randomly:")
print(", ".join(shifted_randomly))
