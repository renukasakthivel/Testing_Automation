import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login_test import login_to_flask_shop  
import pytest

@pytest.fixture(scope="module")
def driver():
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver  # Provide the driver to the test function
    driver.quit()  # Cleanup the driver after tests

# Applying @pytest.mark.usefixtures to ensure the fixture is used in the test functions
@pytest.mark.usefixtures("driver")
def test_check_user_dropdown(driver):
    base_url = "http://127.0.0.1:5000"  
    wait = WebDriverWait(driver, 20)

    try:
        # Navigate to the base URL
        driver.get(base_url)
        
        # Interacting with the user dropdown
        user_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nav-link.dropdown-toggle")))
        user_icon.click()
        time.sleep(1)  # Wait for the dropdown to expand

        username_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='nav-link text-muted']")))
        username = username_element.text.strip().split('\n')[0]  # Just get the name before the rest

        # Check if the "Orders" and "Logout" links are present in the dropdown
        orders_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/orders']")))
        logout_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/logout']")))

        # Optionally, assert or log the results
        assert username == "Expected User Name"  # Example assertion
        print(f"Username: {username}")
        print("Orders link and Logout link are visible in the dropdown.")

    except Exception as e:
        print(f"Error encountered: {e}")

# Main function to run the tests, if needed
if __name__ == "__main__":
    pytest.main(["--html=report.html"])  # Generate the HTML report
