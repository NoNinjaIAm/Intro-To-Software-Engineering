from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize Chrome WebDriver
driver = webdriver.Firefox()

# Navigate to the Home Page
driver.get("http://127.0.0.1:5000/")

cart_icon = driver.find_element(By.NAME, "cart")
cart_icon.click()

remove_item = driver.find_element(By.ID, "minus")
remove_item.click()