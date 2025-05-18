from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time

URL = f"https://www.quintoandar.com.br/alugar/"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Challenge 1
# Dropdown with cities appears after click so is very difficult do a Inspect in the element to can interact using code

# Solution :
# Chrome Console
# > document.querySelector("input[placeholder='Busque por cidade']").click();             -- Click on element
# > document.addEventListener('click', e => e.stopImmediatePropagation(), true);          -- Stop "close" to analisis element on inspector
# >  or  debugger;


SEARCH_TYPE = ['Alugar', 'Comprar']
VALUE_TYPE = ['Valor total', 'Aluguel']
TYPE_OF_HOUSING = ['Apartamento','Casa de Condomínio','Casa', 'Kitnet/Studio']
MIN_NUMBER_OF_BEDROOMS = ['1','2','3','4']
MIN_NUMBER_OF_PARKING_SPACES = ['0','1','2','3']
MIN_NUMBER_OF_BATHROOMS = ['1','2','3','4']
FURNISHED = ['any', 'yes', 'no']
PETS = ['any', 'yes', 'no']
NEAR_SUBWAY = ['any', 'yes', 'no']
AVAILABILITY = ['any', 'immediate', 'soon']
MIN_NUMBER_OF_SUITES = ['0','1','2','3', '4']
CONDOMINIUM_OPTIONS = ["Academia", "Área verde", "Brinquedoteca", "Churrasqueira",
                        "Elevador","Lavanderia", "Piscina", "Playground",
                        "Portaria 24h", "Quadra esportiva", "Salão de festas",
                        "Salão de jogos","Sauna"]

CONVENIENCE_OPTIONS = ["Apartamento cobertura","Ar condicionado", "Banheira", "Box", "Churrasqueira",
                        "Chuveiro a gás", "Closet", "Garden/Área privativa",
                        "Novos ou reformados", "Piscina privativa", "Somente uma casa no terreno",
                        "Tanque", "Televisão", "Utensílios de cozinha", "Ventilador de teto"]

FURNITURE_OPTIONS = ["Armários na cozinha", "Armários no quarto", "Armários nos banheiros",
                        "Cama de casal", "Cama de solteiro","Mesas e cadeiras de jantar","Sofá"]


WEEL_BEING_OPTIONS = ["Janelas grandes", "Rua silenciosa", "Sol da manhã",
                      "Sol da tarde", "Vista livre"]

HOME_APPLIANCES_OPTIONS = ["Fogão", "Fogão cooktop", "Geladeira",
                           "Máquina de lavar", "Microondas"]

ROOMS_OPTIONS = ["Área de serviço", "Cozinha americana", "Home-office",
                 "Jardim", "Quintal", "Varanda"]

ACCESSIBILITY_OPTIONS = ["Banheiro adaptado", "Corrimão", "Piso tátil",
                         "Quartos e corredores com portas amplas",
                          "Rampas de acesso","Vaga de garagem acessível"]

def apply_filter(driver, search_type, value_type, min_value, max_value, type_of_housing,
                 min_number_of_bedrooms,min_number_of_parking_spaces, min_number_of_bathrooms,
                 min_area, max_area, furnished, accept_pets,
                 near_subway, availability, min_number_of_suites,
                 condominium_options, convenience_options, furniture_options,
                 well_being_options, home_appliances_options, rooms_options,
                 accessibility_options):

    # Filters button
    open_filter_button = driver.find_element(By.ID, "cockpit-open-button")
    open_filter_button.click()

    # Search type button
    search_type_button = driver.find_element(By.XPATH, f"//button//span[contains(text(), '{search_type}')]")
    search_type_button.click()

    # Wait until filter form is visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//form[@aria-label='Filtros']"))
    )

    if(search_type == SEARCH_TYPE[0]):
        # Value type
        value_type_button = driver.find_element(By.XPATH, f"//div//span[contains(text(), '{value_type}')]")
        value_type_button.click()

        # Min and Max rent value (First the max value to works)
        max_value_input = driver.find_element(By.ID, "rentPrice-input-max")
        max_value_input.send_keys(Keys.CONTROL + 'a')
        max_value_input.send_keys(Keys.BACKSPACE)
        max_value_input.send_keys(str(max_value))

        min_value_input = driver.find_element(By.ID, "rentPrice-input-min")
        min_value_input.send_keys(Keys.CONTROL + 'a')
        min_value_input.send_keys(Keys.BACKSPACE)
        min_value_input.send_keys(str(min_value))

        # Type of housing
        for type in type_of_housing:
            house_type_checkbox = driver.find_element(By.ID, f"checkbox-{type}")
            house_type_checkbox.click()

        # Number of bedrooms
        min_bedrooms_input =  driver.find_element(By.CSS_SELECTOR, f"label[for='bedrooms-{min_number_of_bedrooms}']")
        min_bedrooms_input.click()

        # Min car spots
        min_parking_spaces_input = driver.find_element(By.CSS_SELECTOR, f"label[for='parkingspaces-{min_number_of_parking_spaces}']")
        min_parking_spaces_input.click()

        # Min bathrooms
        min_bethrooms_input = driver.find_element(By.CSS_SELECTOR,f"label[for='bathrooms-{min_number_of_bathrooms}']")
        min_bethrooms_input.click()

        # Min and max area
        max_value_input = driver.find_element(By.ID, "area-input-max")
        max_value_input.send_keys(Keys.CONTROL + 'a')
        max_value_input.send_keys(Keys.BACKSPACE)
        max_value_input.send_keys(str(max_area))

        min_value_input = driver.find_element(By.ID, "area-input-min")
        min_value_input.send_keys(Keys.CONTROL + 'a')
        min_value_input.send_keys(Keys.BACKSPACE)
        min_value_input.send_keys(str(min_area))

        # Is it furnished ?
        is_furnished_input = driver.find_element(By.CSS_SELECTOR, f"label[for='furnished-{furnished}']")
        is_furnished_input.click()

        # Do you accept pets ?
        accept_pets_input = driver.find_element(By.CSS_SELECTOR, f"label[for='acceptspets-{accept_pets}']")
        accept_pets_input.click()

        # Near to subway ?
        near_subway_input = driver.find_element(By.CSS_SELECTOR, f"label[for='nearsubway-{near_subway}']")
        near_subway_input.click()

        # Availability
        availability_input = driver.find_element(By.CSS_SELECTOR, f"label[for='availability-{availability}']")
        availability_input.click()

        # Min number of suites
        min_number_of_suites_input = driver.find_element(By.CSS_SELECTOR, f"label[for='suites-{min_number_of_suites}']")
        min_number_of_suites_input.click()

        # Condominium
        for option in condominium_options:
            condominium_checkbox = driver.find_element(By.ID, f"checkbox-{option}")
            condominium_checkbox.click()

        # Convenience
        for option in convenience_options:
            convenience_checkbox = driver.find_element(By.ID, f"checkbox-{option}")
            convenience_checkbox.click()
            driver.implicitly_wait(100)

        # Furniture
        for option in furniture_options:
            furniture_checkbox = driver.find_element(By.ID, f"checkbox-{option}")
            furniture_checkbox.click()

        # Well-being
        for option in well_being_options:
            well_being_checkbox = driver.find_element(By.ID, f"checkbox-{option}")
            well_being_checkbox.click()

        # Home appliances
        for option in home_appliances_options:
            home_appliances_checkbox = driver.find_element(By.ID, f"checkbox-{option}")
            home_appliances_checkbox.click()

        # Rooms of the property
        for option in rooms_options:
            rooms_checkbox = driver.find_element(By.ID, f"checkbox-{option}")
            rooms_checkbox.click()

        # Accessibility
        for option in accessibility_options:
            accessibility_checkbox = driver.find_element(By.ID, f"checkbox-{option}")
            accessibility_checkbox.click()

        # Submit button
        driver.implicitly_wait(2000)

        filter_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='apply-filters-btn']")
        number_of_results = filter_button.find_element(By.TAG_NAME, "span")
        print(f"🔍 Number of results: {number_of_results.text.strip()}")
        filter_button.click()

    else:
        pass

    time.sleep(20)

def local_search(driver, city, neighborhood = None , amount = None, number_of_rooms = None):
    # City Input
    city_input = driver.find_element(By.NAME, "landing-city-input")
    city_input.click()
    city_input.send_keys(city)

    # Neighborhood Input
    city_neighborhood = driver.find_element(By.NAME, "landing-neighborhood-input")
    city_neighborhood.click()
    city_neighborhood.send_keys(neighborhood)

    # Search
    search_button = driver.find_element(By.XPATH, "//button[@input-latency='landing-search-button']")
    search_button.click()

    # Skip advertising
    skip_button = driver.find_element(By.XPATH, "//button//span[contains(text(), 'Pular tudo')]")
    skip_button.click()

    driver.implicitly_wait(2000)

def main():

    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless') # ensure GUI is off
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_page_load_timeout(160)
    driver.set_window_size(1600, 1200)

    driver.get(URL)
    driver.implicitly_wait(2000)

    local_search(driver, "São Paulo", "Alto de Pinheiros")

    apply_filter(driver, SEARCH_TYPE[0], VALUE_TYPE[1], '1000', '2000', TYPE_OF_HOUSING,
                 MIN_NUMBER_OF_BEDROOMS[2], MIN_NUMBER_OF_PARKING_SPACES[1], MIN_NUMBER_OF_BATHROOMS[3],
                 70, 120, FURNISHED[1], PETS[1], NEAR_SUBWAY[0], AVAILABILITY[1],MIN_NUMBER_OF_SUITES[-1],
                 CONDOMINIUM_OPTIONS, CONVENIENCE_OPTIONS, FURNITURE_OPTIONS,
                 WEEL_BEING_OPTIONS, HOME_APPLIANCES_OPTIONS, ROOMS_OPTIONS,
                 ACCESSIBILITY_OPTIONS)

    driver.implicitly_wait(2000)
