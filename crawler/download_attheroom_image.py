import io
import os

import pandas as pd
import requests
from PIL import Image
from selenium.webdriver.common.by import By

import browser


def download_image(image_url, save_path):
    try:
        # Set headers (mimic a browser)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        # Download the image
        response = requests.get(image_url, headers=headers, stream=True)

        # Check if the image was retrieved successfully
        if response.status_code == 200:
            # Open the image
            image = Image.open(io.BytesIO(response.content))

            # Convert to RGB (this also converts GIFs, which have an alpha channel, and .webp images)
            image = image.convert("RGB")

            # Save as JPEG
            image.save(save_path, "JPEG")
        else:
            print(f"Image couldn't be retrieved. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


df = pd.read_csv("/Users/treenulbo/Downloads/NUGU_상품마진_상품명만.csv", encoding="utf-8-sig")
data = df["상품명"].to_list()

browser.init_webdriver_pool(1)
driver = browser.generate_chrome_driver()

url = "https://attheroom.com/index.html"
driver.get(url)

for product_name in data:
    product_name = "3줄 진주 레이어드 목걸이 (2color)"
    try:
        input_field = driver.find_elements(By.ID, "keyword")[-1]
        input_field.send_keys(product_name)
        input_field.submit()

        driver.find_element(By.CLASS_NAME, "thumbnail").click()
        browser.selenium_scroll_down_to_end(driver)

        thumbnail = driver.find_element(By.CLASS_NAME, "BigImage").get_attribute("src")
        product_details = driver.find_element(By.ID, "prdDetail")
        sub_images = [
            img.get_attribute("src")
            for img in product_details.find_elements(By.CSS_SELECTOR, "img")
        ][:-1]

        # Base directory where the folders should be created
        base_dir = "/Users/treenulbo/Downloads/attheroom"

        # Construct the full directory path
        dir_path = os.path.join(base_dir, product_name.replace("/", "-"))

        # Check if there are any files in the directory
        if not os.listdir(dir_path):
            # Download and save the main image
            main_image_path = os.path.join(dir_path, "main.jpg")
            download_image(thumbnail, main_image_path)

            # Download and save the sub images
            for i, sub_image in enumerate(sub_images, start=1):
                sub_image_path = os.path.join(dir_path, f"sub_{i}.jpg")
                download_image(sub_image, sub_image_path)

            print(f"Download completed for: {product_name}")
        else:
            print(f"*** Already contains files: {product_name}")
    except Exception as e:
        print(e)
        print(f"### Failed {product_name}")
    break

browser.deinit_webdriver_pool()
