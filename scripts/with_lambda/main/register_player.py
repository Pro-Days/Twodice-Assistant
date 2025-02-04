import misc
import data_manager


def register_player(name, slot=1):

    while uuid := misc.get_uuid_from_mc(name) is None:
        pass

    item = data_manager.read_data("TA_DEV-Users", "uuid-index", uuid=uuid)

    if item is None:  # 등록되지 않은 플레이어
        data_manager.write_data(
            "TA_DEV-Users",
            {
                "id": misc.get_max_id() + 1,
                "name": name,
                "mainSlot": slot,
                "uuid": uuid,
                "lower_name": name.lower(),
            },
        )
    else:  # 등록된 플레이어 (mainSlot만 변경 or 닉네임 변경)
        data_manager.write_data(
            "TA_DEV-Users",
            {
                "id": item[0]["id"],
                "name": name,
                "mainSlot": item[0]["mainSlot"],
                "uuid": uuid,
                "lower_name": name.lower(),
            },
        )


if __name__ == "__main__":
    # print(is_registered("prodays"))
    pass
