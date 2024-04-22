from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize Chrome WebDriver
driver = webdriver.Firefox()

# Navigate to the Home Page
driver.get("http://127.0.0.1:5000/login")

def login():
    username_field = driver.find_element(By.NAME, "username")
    username_field.send_keys("eah123")

    time.sleep(2)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("123")

    time.sleep(2)

    login_button = driver.find_element(By.CLASS_NAME, "loginButton")
    login_button.click()

login()

time.sleep(2)

search_icon = driver.find_element(By.NAME, "search")
search_icon.click()

time.sleep(2)

search_bar = driver.find_element(By.NAME, "query")
search_bar.send_keys("peach")

time.sleep(2)

search_bar.send_keys(Keys.RETURN)

time.sleep(2)
add_item = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "addToCart")))

add_item.click()