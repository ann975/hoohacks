# app.py (Flask example)
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
EXCHANGE_RATE_API_URL = "https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/"

class FlightSearch:
    # Your FlightSearch class implementation here
    # (same as in your Python code)
    pass

@app.route('/api/search-flights', methods=['POST'])
def search_flights():
    data = request.json
    
    # Extract parameters from request
    destination = data.get('destination')
    budget = float(data.get('budget', 0))
    origin = data.get('origin', 'DCA')  # Default to DCA if not provided
    departure_date = data.get('departureDate', datetime.now().strftime('%Y-%m-%d'))
    return_date = data.get('returnDate')
    
    # Initialize flight search
    flight_search = FlightSearch()
    
    # Get cheapest flight
    cheapest_flight = flight_search.get_cheapest_flight(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date
    )
    
    if not cheapest_flight:
        return jsonify({"error": "No flights found"}), 404
    
    # Process flight data
    flight_price = float(cheapest_flight['price']['total'])
    flight_currency = cheapest_flight['price']['currency']
    flight_price_in_usd = flight_search.convert_to_usd(flight_price, flight_currency)
    
    # Check if flight is within budget
    if flight_price_in_usd > budget:
        return jsonify({"error": f"No flights found within budget of ${budget}"}), 404
    
    # Extract flight details
    try:
        airline = cheapest_flight['validatingAirlineCodes'][0]
        segments = cheapest_flight['itineraries'][0]['segments']
        departure_time = segments[0]['departure']['at']
        arrival_time = segments[-1]['arrival']['at']
        stops = len(segments) - 1
        
        # Calculate duration
        departure_datetime = datetime.fromisoformat(departure_time.replace('Z', '+00:00'))
        arrival_datetime = datetime.fromisoformat(arrival_time.replace('Z', '+00:00'))
        duration_seconds = (arrival_datetime - departure_datetime).total_seconds()
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        duration = f"{hours}h {minutes}m"
        
        # Format times for display
        departure_time_formatted = departure_datetime.strftime('%I:%M %p')
        arrival_time_formatted = arrival_datetime.strftime('%I:%M %p')
        
        flight_data = {
            "airline": airline,
            "price": flight_price_in_usd,
            "link": f"https://www.{airline.lower()}.com",  # Placeholder link
            "departureTime": departure_time_formatted,
            "arrivalTime": arrival_time_formatted,
            "duration": duration,
            "stops": stops
        }
        
        return jsonify([flight_data])
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)