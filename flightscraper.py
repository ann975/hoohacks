import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"

class FlightScraper:
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
        if response.status_code == 200:
            print(f"Your token is {response.json()['access_token']}")
            print(f"Your token expires in {response.json()['expires_in']} seconds")
            return response.json()['access_token']
        else:
            print(f"Error fetching token: {response.status_code}")
            return None

    def get_destination_code(self, city_name):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)

        if response.status_code == 200:
            try:
                code = response.json()["data"][0]['iataCode']
                return code
            except IndexError:
                print(f"IndexError: No airport code found for {city_name}.")
                return "N/A"
            except KeyError:
                print(f"KeyError: No airport code found for {city_name}.")
                return "N/A"
        else:
            print(f"Error fetching destination code: {response.status_code}")
            return "N/A"

    def find_flights(self, origin, destination, departure_date, return_date):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": 1,
            "currencyCode": "USD"
        }

        response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=query)

        if response.status_code == 200:
            flight_data = response.json()
            return flight_data
        else:
            print(f"Error fetching flight data: {response.status_code}")
            return None

    def find_lowest_price(self, flight_data):

        if not flight_data or "data" not in flight_data:
            print("No flight offers available.")
            return None

        lowest_price = float('inf')
        lowest_price_flight = None

        for offer in flight_data["data"]:
            price = float(offer["price"]["total"])
            if price < lowest_price:
                lowest_price = price
                lowest_price_flight = offer

        if lowest_price_flight:
            return lowest_price_flight["price"]["total"]
        else:
            return None

if __name__ == "__main__":
    flight_scraper = FlightScraper()

    origin_city = "DCA"  
    destination_city = "LAX"  
    departure_date = "2025-03-01"  
    return_date = "2025-03-05"  

    origin_code = flight_scraper.get_destination_code(origin_city)
    destination_code = flight_scraper.get_destination_code(destination_city)

    if origin_code != "N/A" and destination_code != "N/A":
        flight_data = flight_scraper.find_flights(origin_code, destination_code, departure_date, return_date)
        if flight_data:
            print("Flight Data:")
            print(flight_data)

            lowest_price = flight_scraper.find_lowest_price(flight_data)
            if lowest_price:
                print(f"\nThe lowest price for flights from {origin_city} to {destination_city} from {departure_date} to {return_date} is: ${lowest_price}")
            else:
                print("\nNo flights found with a price.")
        else:
            print("No flight data found.")
    else:
        print("Could not find IATA codes for the given cities.")
