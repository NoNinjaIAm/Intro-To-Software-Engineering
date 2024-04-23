from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize Chrome WebDriver
driver = webdriver.Firefox()

# Navigate to the Login Page
driver.get("http://127.0.0.1:5000/login")

# Login 
username_field = driver.find_element(By.NAME, "username")
username_field.send_keys("eah123")

time.sleep(2)

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("123")

time.sleep(2)

login_button = driver.find_element(By.CLASS_NAME, "loginButton")
login_button.click()