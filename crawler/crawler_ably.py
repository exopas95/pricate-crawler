import platform
import time

import pyperclip
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

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


def update_price(_id, price):
    url = f"https://my.a-bly.com/goods/edit/{_id}"
    driver.get(url)

    time.sleep(3)

    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass

    wait = WebDriverWait(driver, 20)
    price_card = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".price-card"))
    )
    prices = price_card.find_elements(By.CSS_SELECTOR, "form > div")

    discount = prices[2]

    discount_option = discount.find_element(
        By.CSS_SELECTOR, "span.el-radio__input > input"
    )
    if discount_option.is_selected():
        print(f"Discount option already applied: {_id}")
    else:
        driver.execute_script("arguments[0].click();", discount_option)

        discounted_price = discount.find_element(By.CSS_SELECTOR, ".el-input__inner")
        discounted_price.clear()
        clipboard_input(discounted_price, "1000")

        sales_price = prices[1].find_element(By.CSS_SELECTOR, "input")
        sales_price.clear()

        clipboard_input(
            sales_price,
            str(int(price) + 1000),
        )

        driver.find_element(
            By.CSS_SELECTOR, ".el-row > button.el-button.el-button--primary.is-plain"
        ).click()
        print(f"Update complete: {_id}")
        time.sleep(3)

    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass


def process_products():
    print("Scraping start...")

    total_page = 58
    for i in tqdm(range(20, total_page)):
        current_page = i + 1

        product_page_url = f"https://my.a-bly.com/goods/list?page={current_page}"
        driver.get(product_page_url)
        time.sleep(3)

        products_fixed = driver.find_elements(
            By.CSS_SELECTOR, ".el-table__fixed-body-wrapper > table > tbody > tr"
        )
        product_ids = [
            product.find_elements(By.CSS_SELECTOR, "td")[1]
            .find_element(By.CSS_SELECTOR, "span")
            .text
            for product in products_fixed
        ]

        products_body = driver.find_elements(
            By.CSS_SELECTOR, ".el-table__body-wrapper > table > tbody > tr"
        )

        product_prices = [
            product.find_elements(By.CSS_SELECTOR, "td")[6]
            .find_element(By.CSS_SELECTOR, "span")
            .text.replace("원", "")
            .replace(",", "")
            for product in products_body
        ]

        if len(products_fixed) != len(products_body):
            print("Length mismatched...")
            return

        for product_id, price in zip(product_ids, product_prices):
            update_price(product_id, price)


browser.init_webdriver_pool(1)
driver = browser.generate_chrome_driver()

login()
close_popup()
process_products()

browser.deinit_webdriver_pool()
