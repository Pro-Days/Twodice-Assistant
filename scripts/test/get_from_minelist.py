import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


options = Options()
# options.add_argument("--headless")  # 브라우저 창을 표시하지 않음
options.add_argument("--disable-gpu")  # GPU 가속 비활성화
options.add_argument("--no-sandbox")  # 샌드박스 비활성화
options.add_argument(
    "--disable-dev-shm-usage"
)  # /dev/shm 사용 비활성화 (메모리 문제 방지)
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


def get_server_info():
    url = "https://minelist.kr/servers/mineplanet.kr"
    driver.get(url)

    vote = (
        WebDriverWait(driver, 2)
        .until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="content-container"]/div[3]/div[1]/div[2]/div/div[3]/p[1]',
                )
            )
        )
        .text
    )

    print(vote)

    while True:
        time.sleep(1)
    return


if __name__ == "__main__":
    get_server_info()
