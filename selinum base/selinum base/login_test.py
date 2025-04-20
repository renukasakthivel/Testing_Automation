import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Directory to store screenshots
SCREENSHOT_DIR = r"D:\Prototype\selinum base\selinum base\screenshots"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# Helper function to take a screenshot
def take_screenshot(driver, test_name):
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved at: {screenshot_path}")

# Login function
def login_to_flask_shop(driver, base_url, username, password):
    driver.get(f"{base_url}/login")
    driver.maximize_window()

    wait = WebDriverWait(driver, 20)

    username_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
    ActionChains(driver).move_to_element(login_button).click().perform()

    wait.until(EC.url_changes(f"{base_url}/login"))

# Pytest Test Case 1: Test Valid Login
@pytest.mark.parametrize("username, password", [("abc@gmail.com", "abcd@123")])
def test_valid_login(username, password):
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    try:
        login_to_flask_shop(driver, "http://127.0.0.1:5000", username, password)
        assert driver.current_url != "http://127.0.0.1:5000/login", "Login failed, still on login page."
    except Exception as e:
        take_screenshot(driver, "test_valid_login")
        raise e
    finally:
        driver.quit()

# Pytest Test Case 2: Test Invalid Login (Incorrect Email)
@pytest.mark.parametrize("username, password", [("wrongemail@gmail.com", "abcd@123")])
def test_invalid_login_incorrect_email(username, password):
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    try:
        login_to_flask_shop(driver, "http://127.0.0.1:5000", username, password)
        assert driver.current_url == "http://127.0.0.1:5000/login", "Login should fail with incorrect email."
    except Exception as e:
        take_screenshot(driver, "test_invalid_login_incorrect_email")
        raise e
    finally:
        driver.quit()

# Pytest Test Case 3: Test Invalid Login (Incorrect Password)
@pytest.mark.parametrize("username, password", [("abc@gmail.com", "wrongpassword")])
def test_invalid_login_incorrect_password(username, password):
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    try:
        login_to_flask_shop(driver, "http://127.0.0.1:5000", username, password)
        assert driver.current_url == "http://127.0.0.1:5000/login", "Login should fail with incorrect password."
    except Exception as e:
        take_screenshot(driver, "test_invalid_login_incorrect_password")
        raise e
    finally:
        driver.quit()

# Pytest Test Case 4: Test Login with Empty Fields
@pytest.mark.parametrize("username, password", [("", "")])
def test_empty_login_fields(username, password):
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    try:
        login_to_flask_shop(driver, "http://127.0.0.1:5000", username, password)
        assert driver.current_url == "http://127.0.0.1:5000/login", "Login should fail with empty fields."
    except Exception as e:
        take_screenshot(driver, "test_empty_login_fields")
        raise e
    finally:
        driver.quit()

# Pytest Test Case 5: Test Login with Special Characters
@pytest.mark.parametrize("username, password", [("abc!@#gmail.com", "abcd@123!$")])
def test_login_with_special_characters(username, password):
    driver_path = r"C:\Users\Admin\Documents\JATAYU\week3\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    
    try:
        login_to_flask_shop(driver, "http://127.0.0.1:5000", username, password)
        assert driver.current_url != "http://127.0.0.1:5000/login", "Login failed with special characters in credentials."
    except Exception as e:
        take_screenshot(driver, "test_login_with_special_characters")
        raise e
    finally:
        driver.quit()
