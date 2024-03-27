from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Initialize Chrome WebDriver
driver = webdriver.Firefox()

# Navigate to the Home Page
driver.get("http://127.0.0.1:5000/")

cart_icon = driver.find_element(By.NAME, "cart")
cart_icon.click()

proceed_payment = driver.find_element(By.CLASS_NAME, "proceedPayment")
proceed_payment.click()

cardholder_name = driver.find_element(By.ID, "name")
cardholder_name.send_keys("Jimmy Neutron")

card_number = driver.find_element(By.ID, "cardNumber")
card_number.send_keys(1234567890123456)

cvv_number = driver.find_element(By.ID, "cvvNumber")
cvv_number.send_keys(123)

expiration_date = driver.find_element(By.ID, "expDate")
expiration_date.send_keys(52024)

submit_payment = driver.find_element(By.CLASS_NAME, "settingsButton")
submit_payment.click()