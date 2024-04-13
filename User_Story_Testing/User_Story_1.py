from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize Chrome WebDriver
driver = webdriver.Firefox()

# Navigate to the Home Page
driver.get("http://127.0.0.1:5000/")

# Click on the profile icon
profile_icon = driver.find_element(By.CLASS_NAME, "profileButton")
profile_icon.click()

# Click on the "Register a new account" button
register_button = driver.find_element(By.NAME, "register")
register_button.click()

# Fill out the registration form
email_field = driver.find_element(By.NAME, "email")
email_field.send_keys("eah123")

password_field = driver.find_element(By.NAME, "psw")
password_field.send_keys("123")

confirm_password_field = driver.find_element(By.NAME, "psw-repeat")
confirm_password_field.send_keys("123")

# Click the "Create Account" button
create_account_button = driver.find_element(By.CLASS_NAME, "registerbtn")
create_account_button.click()