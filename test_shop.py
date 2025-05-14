import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.usefixtures("login")
def test_add_product_to_cart(browser, base_url):
    """Test adding a product to the shopping cart"""
    # Go to a product page (using Digital downloads as an example)
    browser.get(f"{base_url}/digital-downloads")
    
    # Add the first product to cart
    add_to_cart_button = browser.find_element(By.CSS_SELECTOR, "input[value='Add to cart']")
    add_to_cart_button.click()
    
    # Wait for the cart to update
    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span.cart-qty"), "1")
    )
    
    # Verify the cart has the item
    cart_qty = browser.find_element(By.CSS_SELECTOR, "span.cart-qty").text
    assert "1" in cart_qty

@pytest.mark.usefixtures("login")
def test_complete_shopping(browser, base_url):
    """Test completing the shopping process (checkout)"""
    # First add a product to cart
    browser.get(f"{base_url}/digital-downloads")
    add_to_cart_button = browser.find_element(By.CSS_SELECTOR, "input[value='Add to cart']")
    add_to_cart_button.click()
    
    # Go to shopping cart
    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span.cart-qty"), "1")
    )
    browser.get(f"{base_url}/cart")
    
    # Agree to terms and checkout
    terms_checkbox = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "termsofservice"))
    )
    terms_checkbox.click()
    
    checkout_button = browser.find_element(By.ID, "checkout")
    checkout_button.click()
    
    # Fill in billing address (assuming already saved from registration)
    # Just proceed with the existing address
    continue_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Continue'][onclick='Billing.save()']"))
    )
    continue_button.click()
    
    # Select shipping method
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "shippingoption_1"))
    ).click()
    
    shipping_continue = browser.find_element(By.CSS_SELECTOR, "input[value='Continue'][onclick='ShippingMethod.save()']")
    shipping_continue.click()
    
    # Select payment method
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "paymentmethod_0"))
    ).click()
    
    payment_continue = browser.find_element(By.CSS_SELECTOR, "input[value='Continue'][onclick='PaymentMethod.save()']")
    payment_continue.click()
    
    # Confirm payment info
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Continue'][onclick='PaymentInfo.save()']"))
    ).click()
    
    # Confirm order
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Confirm'][onclick='ConfirmOrder.save()']"))
    ).click()
    
    # Verify order confirmation
    confirmation = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.title strong"))
    )
    assert "Your order has been successfully processed!" in confirmation.text

@pytest.fixture
def login(browser, base_url, registered_user):
    """Fixture to login before shopping tests"""
    browser.get(f"{base_url}/login")
    email = browser.find_element(By.ID, "Email")
    email.send_keys(registered_user["email"])
    password = browser.find_element(By.ID, "Password")
    password.send_keys(registered_user["password"])
    login_button = browser.find_element(By.CSS_SELECTOR, "input[value='Log in']")
    login_button.click()
    yield
