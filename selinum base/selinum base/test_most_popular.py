from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# pytest fixture to set up and tear down the WebDriver
@pytest.fixture(scope="module")
def driver():
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver  # Pass the driver to the test function
    driver.quit()  # Quit the driver after the test is done

# Test function decorated with @pytest.mark
@pytest.mark.usefixtures("driver")
def test_products_section(driver):
    base_url = "http://127.0.0.1:5000"  # URL of your homepage
    driver.get(base_url)  # Open the webpage

    # Set up explicit wait
    wait = WebDriverWait(driver, 20)

    try:
        # Wait for the "New Arrivals" section to be visible
        products_section = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "New Arrivals")]')))
        
        # Find all product cards
        products = driver.find_elements(By.XPATH, "//div[contains(@class, 'card')]")
        
        # Expected products list
        expected_products = [
            "iPhone 12$799.0",
            "iPhone 12 mini$729.0",
            "iPhone 11$699.0",
            "Acer Nitro 5$1300.0",
            "Apple MacBook Pro$1990.0",
            "Mi TV 4X$500.0"
        ]
        
        # Check if all expected products are found
        for product in expected_products:
            found = False
            for element in products:
                # Get product name and price
                product_name = element.find_element(By.CLASS_NAME, "card-title").text
                product_price = element.find_element(By.CLASS_NAME, "card-text").text
                # Match product name and price with expected product
                if product_name + product_price == product:
                    found = True
                    break
            
            # If a product is not found, print a message
            if not found:
                print(f"Product not found: {product}")

    except Exception as e:
        print(f"Test failed with exception: {str(e)}")
        raise e 


if __name__ == "__main__":
    pytest.main()
