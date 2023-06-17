import platform
import time

import pyperclip
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import browser


def clipboard_input(element, user_input):
    temp_user_input = pyperclip.paste()

    pyperclip.copy(user_input)
    element.click()

    if platform.system() == "Darwin":
        ActionChains(driver).key_down(Keys.COMMAND).send_keys("v").key_up(
            Keys.COMMAND
        ).perform()
    else:
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("v").key_up(
            Keys.CONTROL
        ).perform()

    pyperclip.copy(temp_user_input)
    time.sleep(1)


def login():
    print("Logging in...")
    try:
        url = "https://my.a-bly.com/login?redirect=%2Fdashboard"
        uid = "khi5916@naver.com"
        upw = "atroom0431@"

        driver.get(url)
        clipboard_input(driver.find_element(By.NAME, "email"), uid)
        clipboard_input(driver.find_element(By.NAME, "password"), upw)
        driver.find_element(By.CLASS_NAME, "el-button").click()

        return
    except:
        pass

    print("Logged in...")


def close_popup():
    print("Closing popups...")
    condition = True

    while condition:
        try:
            dialogs = driver.find_elements(
                By.CSS_SELECTOR, "div.el-dialog__footer > .dialog-footer > .el-button"
            )
            for dialog in dialogs:
                dialog.click()
        except:
            condition = False

    print("Popup closed...")


def process_products():
    print("Scraping start...")
    product_page_url = "https://my.a-bly.com/goods/list"
    driver.get(product_page_url)
    time.sleep(3)

    products = driver.find_elements(
        By.CSS_SELECTOR,
        ".el-table__fixed > .el-table__fixed-body-wrapper > table > > tbody > .el-table__row",
    )

    for product in products:
        columns = product.find_elements(By.CSS_SELECTOR, "td")
        product_price = int(
            product.text.split("\n")[0].replace("원", "").replace(",", "")
        )

        modify_button = columns[2].find_element(By.CSS_SELECTOR, "button")
        modify_button.click()

        price_card = driver.find_element(
            By.CSS_SELECTOR, "div.el-card.price-card.is-hover-shadow"
        )

        prices = price_card.find_elements(By.CSS_SELECTOR, "form > div")
        sales_price = prices[1]

        clipboard_input(sales_price, product_price + 1000)


browser.init_webdriver_pool(1)
driver = browser.generate_chrome_driver()

login()
close_popup()
process_products()

browser.deinit_webdriver_pool()
