import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_positive(browser, base_url, registered_user):
    """Test successful login"""
    browser.get(f"{base_url}/login")
    
    # Fill in login form
    email = browser.find_element(By.ID, "Email")
    email.send_keys(registered_user["email"])
    
    password = browser.find_element(By.ID, "Password")
    password.send_keys(registered_user["password"])
    
    # Submit login
    login_button = browser.find_element(By.CSS_SELECTOR, "input[value='Log in']")
    login_button.click()
    
    # Verify successful login
    account_link = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "account"))
    )
    assert registered_user["email"] in account_link.text

def test_login_negative_wrong_password(browser, base_url, registered_user):
    """Test login with wrong password (negative case)"""
    browser.get(f"{base_url}/login")
    
    # Fill in login form with wrong password
    email = browser.find_element(By.ID, "Email")
    email.send_keys(registered_user["email"])
    
    password = browser.find_element(By.ID, "Password")
    password.send_keys("WrongPassword123")
    
    # Submit login
    login_button = browser.find_element(By.CSS_SELECTOR, "input[value='Log in']")
    login_button.click()
    
    # Verify error message
    error_message = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "validation-summary-errors"))
    )
    assert "Login was unsuccessful" in error_message.text
