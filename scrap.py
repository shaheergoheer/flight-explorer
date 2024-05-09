from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class FlightScraper:
    def __init__(self):
        pass

    def get_flight_info(self, json_data: dict):

        # Extract data from parsed JSON
        trip_type = json_data['trip_type']
        origin = json_data['origin']
        destination = json_data['destination']
        departure_date = json_data['travel_date']
        if json_data['return_date'] is not None and json_data['return_date'] != 'None':
            return_date = json_data['return_date']
        else:
            return_date = None
         
        if json_data['travel_class'] is not None and json_data['travel_class'] != 'None':
            travel_class = json_data[ 'travel_class']
        else:
            travel_class = 'Economy'
        if json_data['number_of_passengers'] is not None and json_data['number_of_passengers'] != 'None':
            number_of_passengers = json_data['number_of_passengers']
        else:
            number_of_passengers = '1'
        number_of_passengers += 'adults'
        
        # Construct the URL with the extracted data
        if trip_type == 'one-way':
            url = f"https://booking.kayak.com/flights/{origin}-{destination}/{departure_date}/{travel_class}/{number_of_passengers}?sort=bestflight_a"
        elif trip_type == 'round' and return_date:
            url = f"https://booking.kayak.com/flights/{origin}-{destination}/{departure_date}/{return_date}/{travel_class}/{number_of_passengers}?sort=bestflight_a"
        elif trip_type == 'round' and not return_date:
            url = f"https://booking.kayak.com/flights/{origin}-{destination}/{departure_date}/{departure_date}/{travel_class}/{number_of_passengers}?sort=bestflight_a"


        print(url)
        # Configure Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        # Initialize the WebDriver (assuming you have Chrome WebDriver installed)
        driver = webdriver.Chrome()

        # Load the HTML page
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "Base-Results-HorizonResult")))
        # time.sleep(8)
        flights = []

        try:
            print('Finding Flights')
            elements = driver.find_elements(By.CLASS_NAME, "Base-Results-HorizonResult")
            # time.sleep(8)

            if not elements:
                print('No Flights')
                raise Exception("No flights found")
            # Extract information from the found elements
            max_flight_count = 5
            for element in elements:
                
                flights.append(element.text)
                max_flight_count -= 1
                if max_flight_count == 0:
                    break

            return flights
        
        except:
            return None

    

# json_data = {'trip_type': 'one-way', 'travel_date': '2024-05-16', 'return_date': 'None', 'origin': 'LHE', 'destination': 'ISB', 'travel_class': 'First', 'number_of_passengers': 'None'}

# x = get_flight_info(json_data)
# print(x)