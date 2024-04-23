from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize Chrome WebDriver
driver = webdriver.Firefox()

# Navigate to the Login Page
driver.get("http://127.0.0.1:5000/login")

time.sleep(2)

# Click on the "Register a new account" button
wait = WebDriverWait(driver, 10)
register_button = wait.until(EC.element_to_be_clickable((By.NAME, "registerAccount")))
register_button.click()

time.sleep(2)

# Fill out the registration form
# email_field = driver.find_element(By.NAME, "email")
email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
email_field.send_keys("eah123")

time.sleep(2)

# username_field = driver.find_element(By.NAME, "uname")
username_field = wait.until(EC.presence_of_element_located((By.NAME, "uname")))
username_field.send_keys("eah123")

time.sleep(2)

# password_field = driver.find_element(By.NAME, "psw")
password_field = wait.until(EC.presence_of_element_located((By.NAME, "psw")))
password_field.send_keys("123")

time.sleep(2)

# confirm_password_field = driver.find_element(By.NAME, "psw-repeat")
confirm_password_field = wait.until(EC.presence_of_element_located((By.NAME, "psw-repeat")))
confirm_password_field.send_keys("123")

time.sleep(2)

# Click the "Create Account" button
create_account_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "registerbtn")))
create_account_button.click()