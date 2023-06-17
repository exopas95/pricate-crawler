import time
from shutil import which
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService

CHROMEDRIVER_PATH = which("chromedriver")
WINDOW_SIZE = "1920,1080"

_webdriver_pool: List[webdriver.Chrome] = []


def init_webdriver_pool(pool_size: int):
    global _webdriver_pool
    _webdriver_pool = []

    for i in range(pool_size):
        driver = generate_chrome_driver()
        _webdriver_pool.append(driver)


def deinit_webdriver_pool():
    for driver in _webdriver_pool:
        driver.quit()

    _webdriver_pool.clear()


def get_webdriver(index: int) -> webdriver.Chrome:
    if index not in range(len(_webdriver_pool)):
        raise

    return _webdriver_pool[index]


def generate_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incongnito")  # Secret Mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-setuid-sandbox")  # Prevent conflict to uid
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent RAM overflow
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/96.0.4664.110 Safari/537.36"
    )
    # chrome_options.add_argument( f'user-agent={UserAgent(fallback="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)
    # AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36").random}')
    chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)


def selenium_scroll_down_to_end(webdriver, max_count=10):
    scroll_pause_time = (
        1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    )
    screen_height = webdriver.execute_script(
        "return window.screen.height;"
    )  # get the screen height of the web
    i = 1

    while True:
        # scroll one screen height each time
        webdriver.execute_script(
            "window.scrollTo(0, {screen_height}*{i});".format(
                screen_height=screen_height, i=i
            )
        )
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = webdriver.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if screen_height * i > scroll_height or i > max_count:
            break


def selenium_wait_until(webdriver, wait_until, wait_time=10):
    WebDriverWait(webdriver, wait_time).until(wait_until)


def selenium_check_alert(driver):
    try:
        alert = driver.switch_to.alert
        time.sleep(1)
        alert.accept()
        return True
    except:
        return False
