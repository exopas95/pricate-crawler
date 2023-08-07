import time

import pandas as pd
from selenium.webdriver.common.by import By

import browser

df = pd.read_csv("/Users/treenulbo/Downloads/NUGU_상품마진_상품명만.csv", encoding="utf-8-sig")
df["material"] = None
df["size"] = None
data = df["상품명"].to_list()

browser.init_webdriver_pool(1)
driver = browser.generate_chrome_driver()

url = "https://attheroom.com/index.html"
driver.get(url)

for product_name in data:
    try:
        input_field = driver.find_elements(By.ID, "keyword")[-1]
        input_field.send_keys(product_name)
        input_field.submit()
        driver.find_element(By.CLASS_NAME, "thumbnail").click()

        texts = driver.find_element(
            By.CSS_SELECTOR,
            "#Detail_wrap > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(2) > td > pre",
        ).text

        if texts:
            texts = [t.replace("\n", "") for t in texts.split("\n")]

            material = ""
            size = ""

            for i in range(len(texts)):
                if "material" in texts[i]:
                    material = texts[i].replace("material ", "")
                elif "size" in texts[i]:
                    size = texts[i].replace("size ", "")
                    if len(texts) > i + 1:
                        if texts[i + 1]:
                            size = f"{size} {texts[i + 1]}"

            df.loc[df["상품명"] == product_name, "material"] = material
            df.loc[df["상품명"] == product_name, "size"] = size
            print(f"소재 & 사이즈 정보 추가 완료: {product_name}")
        else:
            print(f"소재 & 사이즈 정보 없음: {product_name}")
    except:
        try:
            time.sleep(5)

            input_field = driver.find_elements(By.ID, "keyword")[-1]
            input_field.send_keys(product_name)
            input_field.submit()
            driver.find_element(By.CLASS_NAME, "thumbnail").click()

            texts = driver.find_element(
                By.CSS_SELECTOR,
                "#Detail_wrap > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > table > tbody > tr:nth-child(2) > td > pre",
            ).text.split("\n")

            texts = [t.replace("\n", "") for t in texts]

            material = ""
            size = ""

            for i in range(len(texts)):
                if "material" in texts[i]:
                    material = texts[i].replace("material ", "")
                elif "size" in texts[i]:
                    size = texts[i].replace("size ", "")
                    if texts[i + 1]:
                        size = f"{size} {texts[i + 1]}"

            df.loc[df["상품명"] == product_name, "material"] = material
            df.loc[df["상품명"] == product_name, "size"] = size
            print(f"소재 & 사이즈 정보 추가 완료: {product_name}")
        except:
            print(f"크롤링 실패: {product_name}")
            continue

df.to_csv("/Users/treenulbo/Downloads/NUGU_상품_소재_사이즈.csv", encoding="utf-8-sig")

browser.deinit_webdriver_pool()
