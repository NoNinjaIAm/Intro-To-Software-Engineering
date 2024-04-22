from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

settings_icon = driver.find_element(By.NAME, "settings")
settings_icon.click()

time.sleep(2)

edit_account = driver.find_element(By.NAME, "edit")
edit_account.click()

time.sleep(2)

username_field = driver.find_element(By.NAME, "new_uname")
username_field.send_keys("eah223")

time.sleep(2)

email_field = driver.find_element(By.NAME, "new_email")
email_field.send_keys("eah223")

time.sleep(2)

first_name_field = driver.find_element(By.NAME, "new_fname")
first_name_field.send_keys("Ethan")

time.sleep(2)

last_name_field = driver.find_element(By.NAME, "new_lname")
last_name_field.send_keys("Heverly")

time.sleep(2)

street_field = driver.find_element(By.NAME, "new_street")
street_field.send_keys("123 Sesame Street")

time.sleep(2)

state_field = driver.find_element(By.NAME, "new_state")
state_field.send_keys("New York")

time.sleep(2)

city_field = driver.find_element(By.NAME, "new_city")
city_field.send_keys("New York City")

time.sleep(2)

ZIP_field = driver.find_element(By.NAME, "new_zip")
ZIP_field.send_keys("12345")

time.sleep(2)

card_number_field = driver.find_element(By.NAME, "new_card_num")
card_number_field.send_keys("5827731982407312")

time.sleep(2)

card_holder_field = driver.find_element(By.NAME, "new_cardholder_name")
card_holder_field.send_keys("Ethan Heverly")

time.sleep(2)

expiration_field = driver.find_element(By.NAME, "new_date")
expiration_field.send_keys("12/26")

time.sleep(2)

submit_button = driver.find_element(By.NAME, "new_info")
submit_button.click()