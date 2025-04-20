from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest

# Define the driver fixture
@pytest.fixture(scope="module")
def driver():
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver  # Yield the driver to the tests
    driver.quit()  # Close the driver after the tests are complete

# Define the test function with @pytest.mark.usefixtures
@pytest.mark.usefixtures("driver")
def test_scroll_check_homepage(driver):
    base_url = "http://127.0.0.1:5000"  # Replace with your base URL
    driver.get(base_url)
    driver.maximize_window()

    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for the scroll action to complete

    # Scroll back to the top
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)  # Wait for the scroll action to complete


