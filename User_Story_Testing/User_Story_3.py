from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize Chrome WebDriver
driver = webdriver.Firefox()

# Navigate to the Home Page
driver.get("http://127.0.0.1:5000/")

settings_icon = driver.find_element(By.NAME, "settings")
settings_icon.click()

delete_account_icon = driver.find_element(By.CLASS_NAME, "deleteAccountBut")
delete_account_icon.click()