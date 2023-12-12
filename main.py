from time import sleep
from datetime import datetime
from datetime import timedelta
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def get_web_data(airport_from, airport_to, departure_dt, comeback_dt):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/travel/flights?hl=pt-BR")
    driver.maximize_window()

    # Inserting each flight into the search form and getting the minimum price
    lst_flighs = []
    first = True
    for departure in airport_from:
        for arrival in airport_to:
            print(f"{departure}-{arrival}")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            input_from = ""
            input_to = ""
            for _input in inputs:
                acessible_name = _input.accessible_name
                if "De onde?" in acessible_name:
                    input_from = _input
                if "Para onde?" in acessible_name:
                    input_to = _input

            input_from.clear()
            input_from.send_keys(departure)
            sleep(2)
            dropdown_options = driver.find_elements(By.TAG_NAME, "li")
            dropdown_option = [option for option in dropdown_options if f"\n{departure}\n" in option.text][0]
            dropdown_option.click()

            input_to.clear()
            input_to.send_keys(arrival)
            sleep(2)
            dropdown_options = driver.find_elements(By.CLASS_NAME, "P1pPOe")
            dropdown_option = [option for option in dropdown_options if f"{arrival}" in option.text][0]
            dropdown_option.click()

            if first:
                # Inserting the dates into the search form if first interation
                inputs = driver.find_elements(By.TAG_NAME, "input")
                input_departure = ""
                for _input in inputs:
                    acessible_name = _input.accessible_name
                    if "Partida" in acessible_name:
                        input_departure = _input

                input_departure.click()
                sleep(2)
                inputs = driver.find_elements(By.TAG_NAME, "input")
                input_departure = ""
                input_comeback = ""
                for _input in inputs:
                    acessible_name = _input.accessible_name
                    if "Partida" in acessible_name:
                        input_departure = _input
                    if "Volta" in acessible_name:
                        input_comeback = _input

                sleep(2)
                input_departure.send_keys(departure_dt)
                sleep(2)
                input_comeback.send_keys(comeback_dt)
                sleep(1)
                input_comeback.send_keys(Keys.ENTER)
                sleep(1)
                buttons = driver.find_elements(By.TAG_NAME, "button")

                dt_pickup_conclusion = [button for button in buttons if button.text == "Concluído"][0]
                dt_pickup_conclusion.click()

                search_bt = [button for button in buttons if button.text == "Pesquisar"][0]
                search_bt.click()
                first = False

            sleep(3)
            flights = driver.find_elements(By.CLASS_NAME, "pIav2d")
            if flights:
                lst_flight_prices = []
                for flight in flights:
                    if "R$" in flight.text:
                        price = int(re.search("R\$.+", flight.text).group().split()[1].replace(".", ""))
                        lst_flight_prices.append(price)
                min_price = str(min(lst_flight_prices))
            else:
                min_price = None

            temp_lst = []
            temp_lst.append(datetime.today().strftime("%d/%m/%Y %H:%M:%S"))
            temp_lst.append(departure)
            temp_lst.append(arrival)
            temp_lst.append(departure_dt)
            temp_lst.append(comeback_dt)
            temp_lst.append(min_price)
            lst_flighs.append(temp_lst)
        
    driver.close()
    return lst_flighs

def store_data(lst_flighs):
    print("Inserting collected data into flights.db")
    con = sqlite3.connect("flights.db")
    cur = con.cursor()
    # cur.execute("""CREATE TABLE IF NOT EXISTS flights (search_dt DATETIME, departure_airport NVARCHAR(3),
    #                arrival_airport NVARCHAR(3), departure_dt DATETIME, comeback_dt DATETIME, price INT)""")
    for flight in lst_flighs:
        insert_data = "".join(["'" + data + "'," for data in flight[:-1]])
        if flight[-1] is not None:
            cur.execute(f"""INSERT INTO flights VALUES ({insert_data + flight[-1]});""")
        else:
            cur.execute(f"""INSERT INTO flights VALUES ({insert_data + "NULL"});""")
    con.commit()

if __name__ == '__main__':
    airport_from = ["GRU", "VCP", "GIG", "SSA", "MAO", "POA"]
    airport_to = ["LAX", "LAS", "MIA", "CDG", "LIS", "SYD", "EZE", "SCL", "PEK", "DXB", "MEX", "YYZ", "HND", "CPT", "ORD", "PTY"]
    departure_dt = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
    comeback_dt = (datetime.today() + timedelta(days=5)).strftime("%d/%m/%Y")

    lst_flighs = get_web_data(airport_from, airport_to, departure_dt, comeback_dt)
    store_data(lst_flighs)
