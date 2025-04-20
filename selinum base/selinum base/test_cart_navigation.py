import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login_test import login_to_flask_shop, take_screenshot  # Assuming take_screenshot is defined

BASE_URL = "http://127.0.0.1:5000"
USERNAME = "abc@gmail.com"
PASSWORD = "abcd@123"

# Setup Chrome driver for testing
@pytest.fixture(scope="module")
def driver():
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver  # Yield the driver to be used in the tests
    driver.quit()  # Close the driver after the test is complete

# Function for navigation to the cart
def navigate_to_cart(driver, url):
    wait = WebDriverWait(driver, 20)
    cart_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/cart']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", cart_link)
    driver.execute_script("arguments[0].click();", cart_link)
    time.sleep(1)

# Function to navigate back to the home page
def navigate_to_home(driver):
    wait = WebDriverWait(driver, 20)
    home_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", home_link)
    driver.execute_script("arguments[0].click();", home_link)
    time.sleep(1)

# Function to get cart price details
def get_cart_price_details(driver):
    try:
        wait = WebDriverWait(driver, 20)

        # Wait for price_ids element to load and get its value
        price_ids_element = wait.until(EC.presence_of_element_located((By.NAME, "price_ids")))
        price_ids_value = price_ids_element.get_attribute("value")
        price_ids_value = price_ids_value.replace("'", '"')  # Replace single quotes with double quotes
        price_ids = json.loads(price_ids_value)  # Parse the JSON data

        # Wait for the grand total element and get the text
        grand_total_element = wait.until(EC.presence_of_element_located((By.XPATH, "//strong[text()='Grand Total:']/following-sibling::*[1]")))
        grand_total = grand_total_element.text.strip()

        # Return or print cart details
        print(f"Price IDs: {price_ids}")
        print(f"Grand Total: {grand_total}")
        return price_ids, grand_total

    except Exception as e:
        print(f"Error in get_cart_price_details: {e}")
        return None, None  # Return None if an error occurs

# Test function for cart price details
@pytest.mark.cart
def test_cart_price_details(driver):
    try:
        # Login to the application
        login_to_flask_shop(driver, BASE_URL, USERNAME, PASSWORD)

        # Verify that we're logged in and redirected (check URL after login)
        assert BASE_URL + "/login" not in driver.current_url, "Login page not redirected"
        print(f"Current URL after login: {driver.current_url}")

        # Navigate to the cart
        navigate_to_cart(driver, BASE_URL)

        # Get cart price details
        price_ids, grand_total = get_cart_price_details(driver)

        # Verify that price details are retrieved
        assert price_ids is not None, "Failed to retrieve price IDs"
        assert grand_total is not None, "Failed to retrieve grand total"

        # You can perform further assertions or checks based on the retrieved details
        # For example, check that the grand total is a valid number (if applicable)
        assert grand_total.startswith("$"), "Grand total format is incorrect"

    except Exception as e:
        print(f"Test failed with error: {e}")
        take_screenshot(driver, "test_cart_price_details_failed")  # Capture screenshot on failure
        pytest.fail("Test failed due to exception")
