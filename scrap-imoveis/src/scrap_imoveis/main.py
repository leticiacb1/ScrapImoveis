from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time

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

from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

import pandas as pd
import os

# Some challenges found
# Dropdown with cities appears after click so is very difficult do a Inspect in the element to can interact using code, so because of it, we prefer to stick with the filter solution when entering the search section.

# Non-in-depth Work-Around:
# Chrome Console
# > document.querySelector("input[placeholder='Busque por cidade']").click();             -- Click on element
# > document.addEventListener('click', e => e.stopImmediatePropagation(), true);          -- Stop "close" to analisis element on inspector
# >  or  debugger;


# Setup of constant values needed, ref: www.quintoandar.com.br
URL = f"https://www.quintoandar.com.br/alugar/"

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
    """
    Function that finds and click in all the filters chosen by the user
    """

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
        value_type_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='rentPrice']")
        value_type_button = value_type_div.find_element(By.XPATH, f"//div//span[contains(text(), '{value_type}')]")
        value_type_button.click()

        # Min and Max rent value (First the max value to works)
        max_value_input = value_type_div.find_element(By.ID, "rentPrice-input-max")
        max_value_input.send_keys(Keys.CONTROL + 'a')
        max_value_input.send_keys(Keys.BACKSPACE)
        max_value_input.send_keys(str(max_value))

        min_value_input = value_type_div.find_element(By.ID, "rentPrice-input-min")
        min_value_input.send_keys(Keys.CONTROL + 'a')
        min_value_input.send_keys(Keys.BACKSPACE)
        min_value_input.send_keys(str(min_value))

        # # Type of housing
        house_type_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='houseTypes']")
        for type in type_of_housing:
            house_type_checkbox = house_type_div.find_element(By.ID, f"checkbox-{type}")
            house_type_checkbox.click()
        
        # Number of bedrooms
        bedrooms_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='bedrooms']")
        min_bedrooms_input =  bedrooms_div.find_element(By.CSS_SELECTOR, f"label[for='bedrooms-{min_number_of_bedrooms}']")
        min_bedrooms_input.click()

        # # Min car spots
        parking_spacess_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='parkingSpaces']")
        min_parking_spaces_input = parking_spacess_div.find_element(By.CSS_SELECTOR, f"label[for='parkingspaces-{min_number_of_parking_spaces}']")
        min_parking_spaces_input.click()
        
        # # Min bathrooms
        bathrooms_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='bathrooms']")
        min_bethrooms_input = bathrooms_div.find_element(By.CSS_SELECTOR,f"label[for='bathrooms-{min_number_of_bathrooms}']")
        min_bethrooms_input.click()
        
        # Min and max area
        area_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='area']")
        max_value_input = area_div.find_element(By.ID, "area-input-max")
        max_value_input.send_keys(Keys.CONTROL + 'a')
        max_value_input.send_keys(Keys.BACKSPACE)
        max_value_input.send_keys(str(max_area))

        min_value_input = area_div.find_element(By.ID, "area-input-min")
        min_value_input.send_keys(Keys.CONTROL + 'a')
        min_value_input.send_keys(Keys.BACKSPACE)
        min_value_input.send_keys(str(min_area))
        
        # Is it furnished ?
        furnished_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='furnished']")
        is_furnished_input = furnished_div.find_element(By.CSS_SELECTOR, f"label[for='furnished-{furnished}']")
        is_furnished_input.click()
        #
        # # Do you accept pets ?
        accepts_pets_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='acceptsPets']")
        accept_pets_input = accepts_pets_div.find_element(By.CSS_SELECTOR, f"label[for='acceptspets-{accept_pets}']")
        accept_pets_input.click()
        
        # # Near to subway ?
        near_subway_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='nearSubway']")
        near_subway_input = near_subway_div.find_element(By.CSS_SELECTOR, f"label[for='nearsubway-{near_subway}']")
        near_subway_input.click()
        
        # Availability
        availability_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='availability']")
        availability_input = availability_div.find_element(By.CSS_SELECTOR, f"label[for='availability-{availability}']")
        availability_input.click()
        
        # Min number of suites
        suites_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='suites']")
        min_number_of_suites_input = suites_div.find_element(By.CSS_SELECTOR, f"label[for='suites-{min_number_of_suites}']")
        min_number_of_suites_input.click()
        
        # Condominium
        installations_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='installations']")
        for option in condominium_options:
            condominium_checkbox = installations_div.find_element(By.ID, f"checkbox-{option}")
            condominium_checkbox.click()
        
        # Convenience
        amenities_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='amenities']")
        for option in convenience_options:
            convenience_checkbox = amenities_div.find_element(By.ID, f"checkbox-{option}")
            convenience_checkbox.click()
            driver.implicitly_wait(100)
        
        # Furniture
        furnitures_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='furnitures']")
        for option in furniture_options:
            furniture_checkbox = furnitures_div.find_element(By.ID, f"checkbox-{option}")
            furniture_checkbox.click()
        
        # Well-being
        features_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='features']")
        for option in well_being_options:
            well_being_checkbox = features_div.find_element(By.ID, f"checkbox-{option}")
            well_being_checkbox.click()
        
        # Home appliances
        appliances_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='appliances']")
        for option in home_appliances_options:
            home_appliances_checkbox = appliances_div.find_element(By.ID, f"checkbox-{option}")
            home_appliances_checkbox.click()
        
        # Rooms of the property
        rooms_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='rooms']")
        for option in rooms_options:
            rooms_checkbox = rooms_div.find_element(By.ID, f"checkbox-{option}")
            rooms_checkbox.click()
        
        # Accessibility
        accessibility_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='accessibility']")
        for option in accessibility_options:
            accessibility_checkbox = accessibility_div.find_element(By.ID, f"checkbox-{option}")
            accessibility_checkbox.click()

        # Submit button
        filter_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='apply-filters-btn']")
        filter_button.click()

        driver.implicitly_wait(2000)
    else:
        pass

def check_results(driver):
    """
    Auxilitary function to check for the 'no results' message
    """
    # Check for the 'no results' message
    driver.implicitly_wait(1)
    no_results = driver.find_elements(By.XPATH,
                                      "//h4[contains(text(), 'Nenhum imóvel encontrado')]")
    if no_results:
        print("📭 No results found.")
        return 0, "No results"
    else:
        try:
            number_of_results_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='CONTEXTUAL_SEARCH_TITLE']"))
            )
            number_of_results_span = number_of_results_div.find_element(By.TAG_NAME, "span")
            results_text = number_of_results_span.text.strip()
            print(f"📦 Number of results: {results_text}")
            return results_text, "Have results"
        except TimeoutException:
            print("⏳ Timeout while waiting for the results element.")
            return 0, "No results"

def local_search(driver, city, neighborhood = None , amount = None, number_of_rooms = None):
    """
    Auxilitary function to go to the filters page
    """
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

def load_all_results(driver, result_status):
    """
    If the Quinto Andar website has a See more button, this function permits to create a loop to still click on see more and get all the results

    Args:
        driver (): Driver that holds the information
        result_status (str): The result after the apply filter
    """
    if (result_status != "No results"):
        while True:
            try:
                # Wait until the "see more" button is present and clickable
                try:
                    see_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "see-more")))
                    see_more_button.click()
                    print("Clicked 'see more' button.")
                except StaleElementReferenceException as e:
                    print(e)
                    pass

                # Wait a bit for content to load
                time.sleep(2)
            except TimeoutException or NoSuchElementException:
                # If the button is not found within the timeout, break the loop
                # or
                # If the button is not found, break the loop
                print("'See more' button not found. Stopping clicks.")
                return
    else:
        print(f"No results found")

def combine_parentheses(items):
    """
    Sometimes, Quinto Andar has 2 p elements in the same icons, like, "3 quartos (1 suíte)", this functions auxiliate in getting all these informations

    Args:
        items (list): a list of strings
        
    Returns:
        (list): a list with the concated strings
    """
    result = []
    for item in items:
        if "(" in item.text and result:
            result[-1] += " " + item.text
        else:
            result.append(item.text)
    return result

def extract_data(driver, all_information):
    """
    Extract data from driver

    Args:
        driver (): Driver that holds the information
        all_information (boolean): Always true

    Returns:
        Data (dict)
    """
    print("Begin Extraction ...")

    data = {
        "Link" : [],
        "Total Price": [],
        "Rental Price": [],
        "Features": [],
        "Description": [],
        "Region": [],
        "Subway Near": [],
        "Furnished": [],
        "Pet Friendly": [],
        "Floor": [],
        "Parking Space": [],
        "Bathrooms": [],
        "Rooms": [],
        "Area": []
    }

    key_values = ["Subway Near", "Furnished", "Pet Friendly", "Floor", "Parking Space", "Bathrooms", "Rooms", "Area"]

    house_gris_rows = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='HOUSE_GRID_ROW_CARD_TEST_ID']")

    for row in house_gris_rows:
        house_cards = row.find_elements(By.CSS_SELECTOR, "div[data-testid='house-card-container-rent']")

        for card in house_cards:
            a = card.find_element(By.TAG_NAME, 'a')
            data["Link"].append(a.get_attribute("href"))
            # print(a.get_attribute("href"))

            prices = a.find_elements(By.TAG_NAME, 'p')
            total_price, rental_price =  prices
            data["Total Price"].append(total_price.text)
            data["Rental Price"].append(rental_price.text)

            # print(total_price.text, rental_price.text)

            features = a.find_element(By.TAG_NAME, 'h3')
            data["Features"].append(features.text)

            # print(features.text)

            region = a.find_elements(By.TAG_NAME, 'h2')
            if len(region) == 2:
                data["Description"].append(region[0].text)
                data["Region"].append(region[1].text)
            else:
                data["Description"].append("-")
                data["Region"].append("-")

            if(all_information):
                a.click()

                # New tab
                driver.implicitly_wait(2000)
                driver.switch_to.window(driver.window_handles[1])
                driver.implicitly_wait(5000)

                try:
                    more_info_div = driver.find_element(By.CSS_SELECTOR, "div[data-testid='house-main-info']")
                    infos = more_info_div.find_elements(By.TAG_NAME, 'p')
                    infos = combine_parentheses(infos)
                    for (key, info) in zip(key_values, infos[::-1]):
                        data[key].append(info)
                        
                except StaleElementReferenceException as e:
                    pass
            else:
                pass           
            # Switch back to the original (first) tab
            driver.implicitly_wait(2000)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
    return data

def write_to_excel(data, file_name):
    """
    Auxiliary function to write data to an Excel file. It uses pandas and os as dependencies.

    Args:
        data (dict): Data extracted from web scraping.
        file_name (str): Name of the file to be written.

    Returns:
        None
    """
    df = pd.DataFrame(data)     
    if os.path.exists(file_name):
        print("File exists. Overwriting...")
    else:
        print("File does not exist. Creating a new one...")
    df.to_excel(file_name, index=False)


def loop_question(text, min, max):
    """
    Auxiliary function to create a loop question for search filters

    Args:
        text (str): Question to be made
        min (int): Min range options
        max (int): Max range options
    Returns:
        index (int)
    """
    while True:
        try:
            valor = int(input(text))
            if min <= valor < max:
                return valor
            else:
                print(f"\nPlease use numbers in range {min} to {max-1}")
        except ValueError:
            print(f"\nPlease use numbers in range {min} to {max-1}")

def loop_question_string(text, strings):
    """
    Auxiliary function to create a loop question for search filters

    Args:
        text (str): Question to be made
        strings (list): List of available options
    Returns:
        options (list)
    """
    options = []
    while True:
        try:
            valor = input(text)
            if valor == "all":
                return strings
            elif valor in strings:
                options.append(valor)
            elif valor == "ok":
                return options 
            else:
                print(f"\nVerify if you have already added: {options}")
        except ValueError:
            print(f"\nVerify if you have already added: {options}")

def ask_questions():
    """
    Auxiliary function to to all the questions to the user
    Returns:
        selected_filters (tuple)
    """
    print("\n--- The search for rentals will be carried out on the Quinto Andar website, please answer the following questions: --- \n")
    value_type_int = loop_question("\nDo you want to search by:\n 0 - Total Price\n 1 - Rental Price \n Please use just numbers.\n\n", 0, len(VALUE_TYPE))

    min_value_rent = loop_question("\n--- What is the minimum price you want? [Min value possible = 500]\n", 500, 20001)
    max_value_rent = loop_question("\n--- What is the max price you want? [Max value possible = 20000]\n\n", min_value_rent, 20001)
    
    types_of_housing = loop_question_string(f"\n--- Do you want to filter by: {TYPE_OF_HOUSING}? \n\nIf you want all of them, digit: all, if you already added the options that you want or does not have preference, digit: ok. Please digit the same way as it is shown or else it wont work.\n\n", TYPE_OF_HOUSING)
    
    min_number_bedrooms = loop_question(f"\n--- How many bedrooms do you want? {MIN_NUMBER_OF_BEDROOMS}?\n\n", 1, len(MIN_NUMBER_OF_BEDROOMS)+1) - 1
    min_number_parking = loop_question(f"\n--- How many parking spaces do you want? {MIN_NUMBER_OF_PARKING_SPACES}?\n\n", 0, len(MIN_NUMBER_OF_PARKING_SPACES))
    min_number_bathrooms = loop_question(f"\n--- How many bathrooms do you want? {MIN_NUMBER_OF_BATHROOMS}?\n\n", 1, len(MIN_NUMBER_OF_BATHROOMS)+1) - 1
    
    min_area = loop_question("\n--- What is the minimum area you want? [Min value possible = 20]\n", 20, 1001)
    max_area = loop_question("\n--- What is the max area you want? [Max value possible = 1000]\n", min_area, 1001)
    
    furnished_type_int = loop_question(f"\n--- Do you want to be furnished? \n 0 - any \n 1 - yes \n 2 - no \n Please use just numbers.\n\n", 0, len(FURNISHED))
    pet_type_int = loop_question(f"\n--- Do you want to be pet friendly? \n 0 - any \n 1 - yes \n 2 - no \n Please use just numbers.\n\n", 0, len(PETS))
    near_subway_int = loop_question(f"\n--- Do you want to be near the subway? \n 0 - any \n 1 - yes \n 2 - no \n Please use just numbers.\n\n", 0, len(NEAR_SUBWAY))
    availability_int = loop_question(f"\n--- Do you want to be available in? \n 0 - any \n 1 - immediate \n 2 - soon \n Please use just numbers.\n\n", 0, len(AVAILABILITY))
    min_number_suites = loop_question(f"\n--- How many suites do you want? {MIN_NUMBER_OF_SUITES}?\n\n", 0, len(MIN_NUMBER_OF_SUITES))
    
    condominium_options = loop_question_string(f"\n--- Do you want to filter by: {CONDOMINIUM_OPTIONS}? \n\nIf you want all of them, digit: all, if you already added the options that you want or does not have preference, digit: ok. Please digit the same way as it is shown or else it wont work.\n\n", CONDOMINIUM_OPTIONS)
    convenience_options = loop_question_string(f"\n--- Do you want to filter by: {CONVENIENCE_OPTIONS}? \n\nIf you want all of them, digit: all, if you already added the options that you want or does not have preference, digit: ok. Please digit the same way as it is shown or else it wont work.\n\n", CONVENIENCE_OPTIONS)
    furniture_options = loop_question_string(f"\n--- Do you want to filter by: {FURNITURE_OPTIONS}? \n\nIf you want all of them, digit: all, if you already added the options that you want or does not have preference, digit: ok. Please digit the same way as it is shown or else it wont work.\n\n", FURNITURE_OPTIONS)
    wellbeing_options = loop_question_string(f"\n--- Do you want to filter by: {WEEL_BEING_OPTIONS}? \n\nIf you want all of them, digit: all, if you already added the options that you want or does not have preference, digit: ok. Please digit the same way as it is shown or else it wont work.\n\n", WEEL_BEING_OPTIONS)
    home_appliances_options = loop_question_string(f"\n--- Do you want to filter by: {HOME_APPLIANCES_OPTIONS}?\n\nIf you want all of them, digit: all, if you already added the options that you want or does not have preference, digit: ok. Please digit the same way as it is shown or else it wont work.\n\n", HOME_APPLIANCES_OPTIONS)
    rooms_options = loop_question_string(f"\n--- Do you want to filter by: {ROOMS_OPTIONS}? \nIf you want all of them, digit: all, if you already added the options that you want or does not have preference, digit: ok. Please digit the same way as it is shown or else it wont work.\n\n", ROOMS_OPTIONS)
    accessibility_options = loop_question_string(f"\n--- Do you want to filter by: {ACCESSIBILITY_OPTIONS}? \n\nIf you want all of them, digit: all, if you already added the options that you want or does not have preference, digit: ok. Please digit the same way as it is shown or else it wont work.\n\n", ACCESSIBILITY_OPTIONS)

    return value_type_int, min_value_rent, max_value_rent, types_of_housing, min_number_bedrooms, min_number_parking, min_number_bathrooms, min_area, max_area, furnished_type_int, pet_type_int, near_subway_int, availability_int, min_number_suites, condominium_options, convenience_options,furniture_options, wellbeing_options, home_appliances_options, rooms_options, accessibility_options

def main():
    """
    Main function to do all the logic
    """

    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless') # ensure GUI is off
    #chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--log-level=1")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_page_load_timeout(160)
    driver.set_window_size(1600, 1200)
    
    driver.get(URL)
    driver.implicitly_wait(2000)

    local_search(driver, "São Paulo", "Alto de Pinheiros")

    value_type_int, min_value_rent, max_value_rent, types_of_housing, min_number_bedrooms, min_number_parking, min_number_bathrooms, min_area, max_area, furnished_type_int, pet_type_int, near_subway_int, availability_int, min_number_suites, condominium_options, convenience_options,furniture_options, wellbeing_options, home_appliances_options, rooms_options, accessibility_options  = ask_questions()

    apply_filter(driver, SEARCH_TYPE[0], VALUE_TYPE[value_type_int], min_value_rent, max_value_rent, types_of_housing, MIN_NUMBER_OF_BEDROOMS[min_number_bedrooms], MIN_NUMBER_OF_PARKING_SPACES[min_number_parking], MIN_NUMBER_OF_BATHROOMS[min_number_bathrooms], min_area, max_area, FURNISHED[furnished_type_int], PETS[pet_type_int], NEAR_SUBWAY[near_subway_int], AVAILABILITY[availability_int], MIN_NUMBER_OF_SUITES[min_number_suites], condominium_options, convenience_options,furniture_options, wellbeing_options, home_appliances_options, rooms_options, accessibility_options)

    driver.implicitly_wait(2000)

    number_result, result_status = check_results(driver)

    # Get information on about results
    if number_result != 0:
        load_all_results(driver, result_status)

        driver.implicitly_wait(1000)

        all_information = True
        data = extract_data(driver, all_information)

        file_name = input("\n\n --- Under what name do you want the file to be saved?\n")
        write_to_excel(data, file_name + ".xlsx")

        print(f"\n\nFinished! The results are in the file {file_name}.xlsx\n\n")
        time.sleep(3)
    else:
        print("There was no result for this search!")

    # Quit
    driver.quit()
