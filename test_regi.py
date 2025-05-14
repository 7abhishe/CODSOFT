import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities import generate_random_name, generate_random_lastname

def test_registration_positive(browser, base_url, random_email):
    """Test successful user registration"""
    browser.get(f"{base_url}/register")
    
    # Fill in registration form
    gender = browser.find_element(By.ID, "gender-male")
    gender.click()
    
    first_name = browser.find_element(By.ID, "FirstName")
    first_name.send_keys(generate_random_name())
    
    last_name = browser.find_element(By.ID, "LastName")
    last_name.send_keys(generate_random_lastname())
    
    email = browser.find_element(By.ID, "Email")
    email.send_keys(random_email)
    
    password = browser.find_element(By.ID, "Password")
    password.send_keys("Password123")
    
    confirm_password = browser.find_element(By.ID, "ConfirmPassword")
    confirm_password.send_keys("Password123")
    
    # Submit registration
    register_button = browser.find_element(By.ID, "register-button")
    register_button.click()
    
    # Verify successful registration
    result = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "result"))
    )
    assert "Your registration completed" in result.text

def test_registration_negative_existing_email(browser, base_url, registered_user):
    """Test registration with existing email (negative case)"""
    browser.get(f"{base_url}/register")
    
    # Fill in registration form with existing email
    gender = browser.find_element(By.ID, "gender-male")
    gender.click()
    
    first_name = browser.find_element(By.ID, "FirstName")
    first_name.send_keys("Test")
    
    last_name = browser.find_element(By.ID, "LastName")
    last_name.send_keys("User")
    
    email = browser.find_element(By.ID, "Email")
    email.send_keys(registered_user["email"])
    
    password = browser.find_element(By.ID, "Password")
    password.send_keys("Password123")
    
    confirm_password = browser.find_element(By.ID, "ConfirmPassword")
    confirm_password.send_keys("Password123")
    
    # Submit registration
    register_button = browser.find_element(By.ID, "register-button")
    register_button.click()
    
    # Verify error message
    error_message = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "validation-summary-errors"))
    )
    assert "The specified email already exists" in error_message.text
