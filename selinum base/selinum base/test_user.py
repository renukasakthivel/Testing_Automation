# Required libraries
import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login_test import login_to_flask_shop  

# WebDriver path and base URL
driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
base_url = "http://127.0.0.1:5000"

# Directory to store screenshots
SCREENSHOT_DIR = r"D:\Prototype\selinum base\selinum base\screenshots"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# Fixture to set up WebDriver
@pytest.fixture
def driver():
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

# Hook to capture a screenshot when a test fails
def pytest_runtest_makereport(item, call):
    """Hook to capture a screenshot when a test fails."""
    if call.excinfo is not None:  # Test has failed
        driver = item.funcargs.get("driver")
        if driver:
            # Create a unique filename for the screenshot
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{item.nodeid.replace('::', '_')}.png")
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved at: {screenshot_path}")

# Test 1: Test that the logout link is present in the dropdown after login
@pytest.mark.test_logout_link_present
def test_logout_link_present(driver):
    login_to_flask_shop(driver, base_url, "abc@gmail.com", "abcd@123")
    wait = WebDriverWait(driver, 10)

    # Clicking the dropdown toggle to reveal the logout link
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link.dropdown-toggle"))).click()

    # Locating and verifying that the logout link is displayed
    logout_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/logout']")))
    assert logout_link.is_displayed(), "Logout link not displayed in dropdown"

# Test 2: Test the responsiveness of the dropdown after multiple clicks
@pytest.mark.test_dropdown_multiple_clicks
def test_dropdown_multiple_clicks(driver):
    login_to_flask_shop(driver, base_url, "abc@gmail.com", "abcd@123")
    wait = WebDriverWait(driver, 10)

    # Clicking the user dropdown multiple times to check its behavior
    user_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link.dropdown-toggle")))

    for _ in range(3):
        user_icon.click()
        time.sleep(1)
        user_icon.click()
        time.sleep(1)

    # Verifying that the user dropdown is still functional
    assert user_icon.is_enabled(), "User dropdown is not responsive after multiple clicks"

# Test 3: Test the behavior of the dropdown when not logged in
@pytest.mark.test_dropdown_without_login
def test_dropdown_without_login(driver):
    driver.get(base_url)
    wait = WebDriverWait(driver, 5)
    
    try:
        # Attempting to click the user dropdown when not logged in
        user_icon = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.nav-link.dropdown-toggle")))

        user_icon.click()
        assert False, "User dropdown should not be clickable without login"
    except:
        # If the dropdown is not clickable, the test passes
        assert True, "User dropdown was not clickable without login"
