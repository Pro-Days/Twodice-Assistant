import schedule
import time
import threading


def update_5m():
    print("30m_update")


def update_1d():
    print("1d_update")


def update_10s():
    print("10s_update")


def timer():
    while True:
        schedule.run_pending()
        time.sleep(1)


def update_data():
    schedule.every().hour.at(":05").do(update_5m)
    schedule.every().hour.at(":30").do(update_5m)

    schedule.every().day.at("00:00").do(update_1d)

    threading.Thread(target=timer, daemon=True).start()


if __name__ == "__main__":
    update_data()
