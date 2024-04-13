from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize Chrome WebDriver
driver = webdriver.Firefox()

# Navigate to the Home Page
driver.get("http://127.0.0.1:5000/")

settings_icon = driver.find_element(By.NAME, "settings")
settings_icon.click()

edit_account = driver.find_element(By.NAME, "edit")
edit_account.click()

email_field = driver.find_element(By.NAME, "new_email")
email_field.send_keys("jn@yahoo.com")

address_field = driver.find_element(By.NAME, "new_address")
address_field.send_keys("123 Sesame Street")

state_field = driver.find_element(By.NAME, "new_state")
state_field.send_keys("New York")

city_field = driver.find_element(By.NAME, "new_city")
city_field.send_keys("New York City")

ZIP_field = driver.find_element(By.NAME, "new_zip")
ZIP_field.send_keys("12345")

submit_button = driver.find_element(By.NAME, "new_info")
submit_button.click()