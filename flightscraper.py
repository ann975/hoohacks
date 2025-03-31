import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime  

load_dotenv()  

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
EXCHANGE_RATE_API_URL = "https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/"    

class FlightSearch:    
    def __init__(self):        
        self._api_key = os.environ["AMADEUS_API_KEY"]        
        self._api_secret = os.environ["AMADEUS_SECRET"]        
        self._token = self._get_new_token()  
    
    def _get_new_token(self):        
        header = {            
            'Content-Type': 'application/x-www-form-urlencoded'        
        }        
        body = {            
            'grant_type': 'client_credentials',            
            'client_id': self._api_key,            
            'client_secret': self._api_secret        
        }        
        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)        
        return response.json()['access_token']  
    
    def convert_to_usd(self, amount, currency):        
        """        
        Converts the amount from any currency to USD using the Exchange Rate API.        
        """        
        if currency == "USD":            
            return amount    
        
        response = requests.get(f"{EXCHANGE_RATE_API_URL}{currency}")        
        if response.status_code == 200:            
            exchange_data = response.json()            
            conversion_rate = exchange_data["conversion_rates"].get("USD")            
            if conversion_rate:                
                return amount * conversion_rate            
            else:                
                print(f"Error: Conversion rate for {currency} to USD not found.")                
                return amount        
        else:            
            print(f"Error: Failed to get exchange rate for {currency}.")            
            return amount  
    
    def get_cheapest_flight(self, origin, destination, departure_date, return_date=None):        
        """        
        Retrieves the cheapest flight between two cities for specific dates using the Amadeus Flight API.        
        Parameters:        
        origin (str): The IATA code of the departure city.        
        destination (str): The IATA code of the arrival city.        
        departure_date (str): The departure date in format YYYY-MM-DD.        
        return_date (str, optional): The return date in format YYYY-MM-DD.        
        Returns:        
        dict: The cheapest flight details.        
        """        
        headers = {"Authorization": f"Bearer {self._token}"}        
        query = {            
            "originLocationCode": origin,            
            "destinationLocationCode": destination,            
            "departureDate": departure_date,            
            "adults": 1,            
            "max": 1          
        }  
        
        if return_date:            
            query["returnDate"] = return_date  
        
        response = requests.get(            
            url=FLIGHT_ENDPOINT,            
            headers=headers,            
            params=query        
        )  
        
        if response.status_code == 200:            
            flight_data = response.json()            
            if flight_data['data']:                
                cheapest_flight = flight_data['data'][0]                  
                return cheapest_flight            
            else:                
                print("No flights found.")                
                return None        
        else:            
            print(f"Error: {response.status_code} - {response.text}")            
            return None  

def is_valid_date(date_string):    
    """    
    Validates the date format (YYYY-MM-DD).    
    Returns True if the format is valid, else False.    
    """    
    try:        
        datetime.strptime(date_string, '%Y-%m-%d')        
        return True    
    except ValueError:        
        return False

def is_valid_iata_code(code):
    """
    Validates if the input is a valid IATA airport code format (3 uppercase letters).
    """
    return bool(code and len(code) == 3 and code.isalpha())

def main():    
    flight_search = FlightSearch()  
    
    origin_code = input("Please enter the origin airport code (e.g., DCA): ").upper()
    while not is_valid_iata_code(origin_code):
        origin_code = input("Invalid airport code. Please enter a valid 3-letter IATA code: ").upper()
    
    destination_code = input("Please enter the destination airport code (e.g., LAX): ").upper()
    while not is_valid_iata_code(destination_code):
        destination_code = input("Invalid airport code. Please enter a valid 3-letter IATA code: ").upper()
    
    departure_date = input("Please enter the departure date (YYYY-MM-DD): ")    
    while not is_valid_date(departure_date):        
        departure_date = input("Invalid date format. Please enter the departure date (YYYY-MM-DD): ")  
    
    return_date = input("Please enter the return date (YYYY-MM-DD), or press Enter to skip: ")    
    if return_date and not is_valid_date(return_date):        
        while not is_valid_date(return_date):            
            return_date = input("Invalid date format. Please enter the return date (YYYY-MM-DD), or press Enter to skip: ")  
    
    cheapest_flight = flight_search.get_cheapest_flight(        
        origin=origin_code,        
        destination=destination_code,        
        departure_date=departure_date,        
        return_date=return_date if return_date else None    
    )  
    
    if cheapest_flight:        
        print(f"Cheapest Flight Details:")        
        print(f"Origin: {origin_code}")        
        print(f"Destination: {destination_code}")        
        print(f"Departure Date: {departure_date}")        
        print(f"Return Date: {return_date if return_date else 'N/A'}")  
    
        flight_price = cheapest_flight['price']['total']        
        flight_currency = cheapest_flight['price']['currency']        
        flight_price_in_usd = flight_search.convert_to_usd(float(flight_price), flight_currency)  
    
        print(f"Price: {flight_price_in_usd:.2f} USD")        
        print(f"Airline: {cheapest_flight['validatingAirlineCodes'][0]}")            
        try:            
            flight_number = cheapest_flight['itineraries'][0]['segments'][0]['flightSegment']['marketingCarrier']['flightNumber']            
            print(f"Flight Number: {flight_number}")        
        except KeyError as e:            
            print(f"Error extracting flight number: {e}")            
            print("Details available in response data:")            
            print(cheapest_flight)  
    
        with open("cheapest_flight.json", "w") as json_file:            
            json.dump(cheapest_flight, json_file, indent=4)  
    
        print(f"\nThe cheapest flight price from {origin_code} to {destination_code} is {flight_price_in_usd:.2f} USD.")  
    
    else:        
        print("Could not find any flights.")  

if __name__ == "__main__":    
    main()