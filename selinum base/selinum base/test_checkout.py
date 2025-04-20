import time
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login_test import login_to_flask_shop, take_screenshot  


# Fixture to initialize and quit the driver
@pytest.fixture(scope="module")
def driver():
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()


# Test function to navigate to the cart and check checkout button visibility
@pytest.mark.cart_checkout  # Custom marker to group/cart this test
def test_cart_checkout_button(driver):
    base_url = "http://127.0.0.1:5000"
    
    # Login to the application
    login_to_flask_shop(driver, base_url, "abc@gmail.com", "abcd@123")
    
    # Navigate to the cart and check if the checkout button is visible
    try:
        assert navigate_to_cart(driver, base_url), "Failed to navigate to cart or checkout button not visible."
    except AssertionError as e:
        take_screenshot(driver, "test_cart_checkout_button")  # Call take_screenshot on failure
        raise e  # Re-raise the assertion error after taking screenshot


# Utility function – no decorator needed
def navigate_to_cart(driver, base_url):
    wait = WebDriverWait(driver, 20)
    
    try:
        # Wait for the cart link to be clickable
        cart_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/cart']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", cart_link)
        driver.execute_script("arguments[0].click();", cart_link)
        print("Cart link clicked successfully.")
    except Exception as e:
        print(f"Error while clicking the cart link: {e}")
        take_screenshot(driver, "navigate_to_cart")  # Take screenshot in case of error
        return False

    try:
        # Wait for the checkout button to be visible
        checkout_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Checkout')]")))
        if checkout_button.is_displayed():
            print("Checkout button is visible.")
            return True
        else:
            print("Checkout button is not visible.")
            take_screenshot(driver, "navigate_to_cart_checkout_button")  # Take screenshot if button not visible
            return False
    except Exception as e:
        print(f"Error while checking checkout button visibility: {e}")
        take_screenshot(driver, "navigate_to_cart_checkout_button")  # Take screenshot in case of error
        return False
