import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utilities import generate_random_email

@pytest.fixture(scope="function")
def browser():
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    yield driver
    
    # Teardown
    driver.quit()

@pytest.fixture
def base_url():
    return "https://demowebshop.tricentis.com"

@pytest.fixture
def registered_user():
    return {
        "email": "testuser@example.com",
        "password": "Password123"
    }

@pytest.fixture
def random_email():
    return generate_random_email()
