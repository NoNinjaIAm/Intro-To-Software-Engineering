from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize Chrome WebDriver
driver = webdriver.Firefox()

# Navigate to the Home Page
driver.get("http://127.0.0.1:5000/")

search_icon = driver.find_element(By.NAME, "search")
search_icon.click()

search_bar = driver.find_element(By.NAME, "query")
search_bar.send_keys("Laptop")
search_bar.send_keys(Keys.RETURN)

#For some reason this cannot find element. Come Back later
add_item = driver.find_element(By.NAME, "action")
add_item.click()