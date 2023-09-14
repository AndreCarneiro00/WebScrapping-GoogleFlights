import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()

driver.get("https://www.google.com/travel/flights?hl=pt-BR")
driver.maximize_window()

inputs = driver.find_elements(By.TAG_NAME, "input")
input_from = ""
input_to = ""
input_departure = ""
for _input in inputs:
    acessible_name = _input.accessible_name
    if "De onde?" in acessible_name:
        input_from = _input
    if "Para onde?" in acessible_name:
        input_to = _input
    if "Partida" in acessible_name:
        input_departure = _input

departure = "GRU"
arrival = "LAX"
dt_departure = "20/09/2023"
dt_comeback = "25/09/2023"

input_from.clear()
input_from.send_keys(departure)
time.sleep(1)
dropdown_options = driver.find_elements(By.TAG_NAME, "li")
dropdown_option = [option for option in dropdown_options if f"\n{departure}\n" in option.text][0]
dropdown_option.click()

input_to.send_keys(arrival)
time.sleep(1)
dropdown_options = driver.find_elements(By.CLASS_NAME, "P1pPOe")
dropdown_option = [option for option in dropdown_options if f"{arrival}" in option.text][0]
dropdown_option.click()

input_departure.click()
inputs = driver.find_elements(By.TAG_NAME, "input")
input_departure = ""
input_comeback = ""
for _input in inputs:
    acessible_name = _input.accessible_name
    if "Partida" in acessible_name:
        input_departure = _input
    if "Volta" in acessible_name:
        input_comeback = _input
input_departure.send_keys(dt_departure)
input_comeback.send_keys(dt_comeback)
input_comeback.send_keys(Keys.ENTER)
buttons = driver.find_elements(By.TAG_NAME, "button")

dt_pickup_conclusion = [button for button in buttons if button.text == "Concluído"][0]
dt_pickup_conclusion.click()

search_button = [button for button in buttons if button.accessible_name == "Pesquisar"][0]
search_button.click()

time.sleep(3)
flights = driver.find_elements(By.CLASS_NAME, "pIav2d")

driver.close()



# dt_pickup_conclusion = [button for button in buttons if button.accessible_name == "Concluído"][0]
# dt_pickup_conclusion.click()
# WebDriverWait(driver, 10).until(EC.presence_of_element_located(input_departure)).send_keys(dt_departure)




# time.sleep(5)
# input_departure.send_keys(dt_departure)
#
# time.sleep(5)
# input_comeback.send_keys(dt_comeback)
