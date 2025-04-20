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
    yield driver  # Yield the driver to be used in the tests
    driver.quit()  # Close the driver after the tests are complete

# Define the test function
@pytest.mark.usefixtures("driver")
def test_products_found(driver):
    base_url = "http://127.0.0.1:5000"  # Replace with your actual base URL
    driver.get(base_url)

    try:
        # Wait for the elements to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".items a"))
        )
        print("✅ Products found!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# If you want to generate an HTML report for the tests
if __name__ == "__main__":
    pytest.main(["--html=report.html"])  # This will run the tests and generate an HTML report
