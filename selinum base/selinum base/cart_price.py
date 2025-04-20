import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login_test import login_to_flask_shop, take_screenshot  # Importing the take_screenshot function
from test_cart_navigation import navigate_to_cart  

# Function to get cart price details
def get_cart_price_details(driver):
    try:
        wait = WebDriverWait(driver, 20)

        price_ids_element = wait.until(EC.presence_of_element_located((By.NAME, "price_ids")))
        price_ids_value = price_ids_element.get_attribute("value")
        price_ids_value = price_ids_value.replace("'", '"')
        price_ids = json.loads(price_ids_value)

        grand_total_element = wait.until(EC.presence_of_element_located((By.XPATH, "//strong[text()='Grand Total:']/following-sibling::*[1]")))
        grand_total = grand_total_element.text.strip()

        print(f"Price IDs: {price_ids}")
        print(f"Grand Total: {grand_total}")

    except Exception as e:
        print(f"Error occurred: {e}")
        take_screenshot(driver, "cart_price_error")  # Capture screenshot on error
        driver.quit()

# Test function to verify cart price details
@pytest.mark.cart
def test_cart_price_details():
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        login_to_flask_shop(driver, "http://127.0.0.1:5000", "abc@gmail.com", "abcd@123")
        navigate_to_cart(driver, "http://127.0.0.1:5000")
        get_cart_price_details(driver)

    except Exception as e:
        print(f"Test failed with error: {e}")
        take_screenshot(driver, "test_cart_price_details_failed")  # Capture screenshot on failure
        pytest.fail("Test failed due to exception")

    finally:
        driver.quit()

# You can run the test by using `pytest` from the command line
# Command: pytest <script_name>.py
