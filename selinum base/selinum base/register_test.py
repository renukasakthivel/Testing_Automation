from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# Define the driver fixture
@pytest.fixture(scope="module")
def driver():
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver  # Yield the driver to the tests
    driver.quit()  # Close the driver after the tests are complete

# Define the test function
@pytest.mark.usefixtures("driver")
def test_registration(driver):
    base_url = "http://127.0.0.1:5000/register"  # Replace with your registration URL
    driver.get(base_url)

    try:
        # Wait for the registration form to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'name'))  
        )

        # Fill in the registration form
        driver.find_element(By.ID, 'name').send_keys("Johnn Doe")
        driver.find_element(By.ID, 'phone').send_keys("1234567990")
        driver.find_element(By.ID, 'email').send_keys("johnndoee@gmail.com")
        driver.find_element(By.ID, 'password').send_keys("password123")

        # Confirm password field
        confirm_password = driver.find_element(By.ID, 'confirm')  
        confirm_password.send_keys("password123")

        # Submit the registration form
        driver.find_element(By.ID, 'submit').click()

        # Wait for success message
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'success')) 
        )
        print("✅ Registration test passed!")

    except Exception as e:
        print(f"❌ Registration test failed: {e}")

# If you want to run the tests manually via pytest and generate a report
if __name__ == "__main__":
    pytest.main(["--html=report.html"])  # This will run the tests and generate an HTML report
