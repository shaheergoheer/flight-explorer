import google.generativeai as genai
import json
import time

class GenAI:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_json_content(self, prompt):
        max_retries = 3
        while max_retries != 0:
            try:
                response = self.model.generate_content(prompt)
                time.sleep(2)
                json_string = response.text
                json_string = json_string.split("JSON")[1].replace("```", "")
                json_data = json.loads(json_string)
                if not json_data:
                    max_retries -= 1
                else:
                    break
            except:
                pass
        return json_data

    def get_parsed_input(self, text):
        system_prompt = "Given user text input, your task is to extract relevant travel information such as the trip_type (one-way or round. Do not write anything other then these tokens for trip type) , travel_date, return_date, origin, destination, travel_class (Economy, Business, or First), and number_of_passengers, and format it into JSON. \
            Convert origin and destination into city abbreviations if they are not. \
            If any information is not given, initialize it as None in JSON. \
            You should understand natural language inputs and accurately identify the required details.\
            Dates should be parsed and formatted in the YYYY-MM-DD format."
        prompt = f"{system_prompt}. User input is : {text}"
        return self.generate_json_content(prompt)

    def parse_flight_info(self, flights_data):
        system_prompt = "Given a list of flight details, your task is to convert the list into a human-readable format.\
            Each element in the list represents details of a flight, including airline, departure time, departure airport, arrival time, arrival airport, duration, price, and additional information. \
            Details may also be of round trip flights. \
            You should parse each element and format the flight information into a clear and understandable format."
        prompt = f"{system_prompt}. This is list of flight details : {flights_data}"
        response = self.model.generate_content(prompt)
        formatted_response = response.text
        return formatted_response

# Usage examples:
# parsed_input = flight_assistant.get_parsed_input("User's input text")
# formatted_flight_info = flight_assistant.parse_flight_info(flights_data)
