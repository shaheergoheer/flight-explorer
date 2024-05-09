from fastapi import FastAPI, HTTPException
import base_models, gemini_ai, scrap, constants
import uvicorn

app = FastAPI()

@app.post("/flights-information")
async def flights_information_endpoint(user_input: base_models.UserTextInput):

    ai_model = gemini_ai.GenAI(constants.GOOGLE_API_KEY)
    scrapper = scrap.FlightScraper()

    # Parse given text input into JSON using AI model
    parsed_info = ai_model.get_parsed_input(user_input.text)
    print()
    print('Parsed Info:',parsed_info,'\n')

    # Scrap flights information from internet
    flights = scrapper.get_flight_info(json_data=parsed_info)
    # print(flights)
    if flights:
        response = ai_model.parse_flight_info(flights)
        # print(response)
        return {'ai_model_response':response}
    else:
        raise HTTPException(status_code=404, detail="No flights found")
    


if __name__ == "__main__":
    
    uvicorn.run("init:app", host = "127.0.0.1", port = 8000, reload = True)
