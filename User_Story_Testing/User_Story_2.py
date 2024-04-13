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

username_field = driver.find_element(By.NAME, "uname")
username_field.send_keys("eah123")

password_field = driver.find_element(By.NAME, "psw")
password_field.send_keys("123")

login_button = driver.find_element(By.CLASS_NAME, "loginButton")
login_button.click()