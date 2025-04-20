from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# Define the fixture for setting up the WebDriver
@pytest.fixture(scope="module")
def driver():
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver  # Yield the driver to be used in tests
    driver.quit()  # Ensure that the driver is closed after the test

# Use pytest.mark.usefixtures to indicate that the 'driver' fixture should be used in the test
@pytest.mark.usefixtures("driver")
def test_new_arrivals(driver):
    base_url = "http://127.0.0.1:5000"  # URL of your homepage
    driver.get(base_url)  # Open the webpage

    # Set up explicit wait
    wait = WebDriverWait(driver, 20)

    try:
        # Wait for the "New Arrivals" section to be visible
        new_arrivals_section = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "New Arrivals")]')))
        
        # Find all product names
        products = driver.find_elements(By.XPATH, "//div[contains(@class, 'product-name')]")
        
        # Expected products list
        expected_products = [
            "Mi TV 4X",
            "Apple MacBook Pro",
            "Acer Nitro 5",
            "iPhone 11",
            "iPhone 12 mini",
            "iPhone 12"
        ]
        
        # Check if all expected products are found
        for product in expected_products:
            found = False
            for element in products:
                if product in element.text:
                    found = True
                    break
            
            # If a product is not found, print a message
            if not found:
                print(f"Product not found: {product}")

    except Exception as e:
        print(f"Test failed with exception: {str(e)}")
        raise e  # Reraise the exception to ensure pytest reports the failure

# Run the tests using pytest
if __name__ == "__main__":
    pytest.main()
