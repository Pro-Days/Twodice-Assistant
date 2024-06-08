import os
import json
import misc
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument("--headless")  # 브라우저 창을 표시하지 않음
options.add_argument("--disable-gpu")  # GPU 가속 비활성화
options.add_argument("--no-sandbox")  # 샌드박스 비활성화
options.add_argument(
    "--disable-dev-shm-usage"
)  # /dev/shm 사용 비활성화 (메모리 문제 방지)
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def hanwol(ans):
    ans_json = json.loads(ans)

    if ans_json["fn_id"] == 1:
        (vote, pl), image = get_server_info()
        print(f"vote: {vote}, pl: {pl}, image: {image}")
        os.remove(image)
        return vote, pl, image


def get_server_info(image=True):
    try:
        url = "https://mine.page/server/mineplanet.kr"
        driver.get(url)

        vote = (
            WebDriverWait(driver, 4)
            .until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="app"]/div[3]/div[1]/div[1]/section/div[2]/div[3]/ul/li[4]/p',
                    )
                )
            )
            .text
        )
        vote = int(vote)

        pl = (
            WebDriverWait(driver, 4)
            .until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="app"]/div[3]/div[1]/div[1]/section/div[2]/div[3]/ul/li[2]/p',
                    )
                )
            )
            .text
        )
        pl = pl.split("/")[0]
        pl = int(pl)

        info = (vote, pl)

    except:
        info = (None, None)

    if image:
        image_url = "https://minelist.kr/servers/8117/banner/modern.png"

        try:
            response = requests.get(image_url)
            image_path = misc.convert_path("assets\\images\\minelist_info.png")
            os.makedirs(
                os.path.dirname(image_path),
                exist_ok=True,
            )
            with open(image_path, "wb") as f:
                f.write(response.content)

        except requests.exceptions.RequestException as e:
            image_path = None

        return info, image_path

    else:
        return info, None


if __name__ == "__main__":
    hanwol('{ "fn_id": 1, "q": false, "text": null, "var": {} }')
