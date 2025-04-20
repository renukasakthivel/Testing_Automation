import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from login_test import login_to_flask_shop  # Importing the function from login_test.py

@pytest.fixture(scope="module")
def driver():
    driver_path =r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver  # Yield the driver to be used in the tests
    driver.quit()  # Close the driver after the test is complete


@pytest.mark.parametrize("credentials", [
    {"username": "example1@gmail.com", "password": "example1@123"},
    {"username": "example2@gmail.com", "password": "example2@123"},
    {"username": "example3@gmail.com", "password": "example3@123"}
])
def test_login(driver, credentials):
    base_url = "http://127.0.0.1:5000"  # Replace with your actual base URL

    try:
        print(f"Running test with: {credentials['username']}")
        login_to_flask_shop(driver, base_url, credentials["username"], credentials["password"])
        print(f"✅ Login successful for {credentials['username']}")
    except Exception as e:
        print(f"❌ Login failed for {credentials['username']}: {e}")
