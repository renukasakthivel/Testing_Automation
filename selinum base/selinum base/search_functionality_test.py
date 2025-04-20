import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from login_test import take_screenshot  # Import the screenshot function
import os

# Directory to save screenshots
SCREENSHOT_DIR = r"D:\Prototype\selinum base\selinum base\screenshots"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# WebDriver path
driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
base_url = "http://127.0.0.1:5000"

@pytest.fixture
def setup_browser():
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(base_url)
    yield driver
    driver.quit()

# Function to capture screenshots on failure
def capture_screenshot(driver, test_name):
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
    take_screenshot(driver, screenshot_path)
    print(f"Screenshot saved at {screenshot_path}")

# Test Case 1: Search input field is visible
def test_search_input_is_visible(setup_browser):
    driver = setup_browser
    try:
        search_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="search"][name="query"]'))
        )
        assert search_input.is_displayed(), "Search input field is not visible."
    except Exception as e:
        capture_screenshot(driver, "search_input_visibility_failed")  # Capture screenshot on failure
        assert False, f"Test failed: {str(e)}"

# Test Case 2: Search button is visible and clickable
def test_search_button_is_visible_and_enabled(setup_browser):
    driver = setup_browser
    try:
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"][value="Search"]'))
        )
        assert search_button.is_displayed(), "Search button is not visible."
        assert search_button.is_enabled(), "Search button is not enabled."
    except Exception as e:
        capture_screenshot(driver, "search_button_visibility_failed")  # Capture screenshot on failure
        assert False, f"Test failed: {str(e)}"

# Test Case 3: Search with valid keyword (e.g., "laptop")
def test_valid_search_functionality(setup_browser):
    driver = setup_browser
    try:
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="search"][name="query"]'))
        )
        search_input.send_keys("Apple Macbook pro")
        search_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Search"]')
        search_button.click()

        # Wait for the results and assert if the page source contains the term "laptop"
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))  # Example of waiting for any results page to load
        )
        assert "laptop" in driver.page_source.lower(), "Search results for 'laptop' not found."
    except Exception as e:
        capture_screenshot(driver, "valid_search_failed")  # Capture screenshot on failure
        assert False, f"Test failed: {str(e)}"

# Test Case 4: Search with empty input
def test_empty_search_input(setup_browser):
    driver = setup_browser
    try:
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="search"][name="query"]'))
        )
        search_input.send_keys("")
        search_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Search"]')
        search_button.click()

        # Wait for a message indicating no search term was entered or invalid search
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message"))  # Assuming an error message for empty input
        )
        assert "Please enter a search term" in driver.page_source, "Empty search input did not trigger the correct message."
    except Exception as e:
        capture_screenshot(driver, "empty_search_failed")  # Capture screenshot on failure
        assert False, f"Test failed: {str(e)}"

# Test Case 5: Search with special characters
def test_special_character_search(setup_browser):
    driver = setup_browser
    try:
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="search"][name="query"]'))
        )
        search_input.send_keys("@#$%^&*")
        search_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Search"]')
        search_button.click()

        # Wait for a response indicating no results found or an appropriate message
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))  # Example of checking for a result page header
        )
        assert "no results" in driver.page_source.lower() or "not found" in driver.page_source.lower(), \
            "Special character search did not return an appropriate message."
    except Exception as e:
        capture_screenshot(driver, "special_character_search_failed")  # Capture screenshot on failure
        assert False, f"Test failed: {str(e)}"
