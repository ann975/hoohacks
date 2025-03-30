import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "../styles.css";
import "./Results.css";
import catAirplaneGif from "./cat-airplane.gif";
import catLogo from "./cat-logo.jpg";

interface Flight {
  airline: string;
  price: number;
  link: string;
  departureTime: string;
  arrivalTime: string;
  duration: string;
  stops: number;
}

const Results = () => {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const origin = params.get("origin") || "DCA";
  const destination = params.get("destination") || "";
  const budget = params.get("budget") || "300";
  const departureDate = params.get("departureDate") || "";
  const returnDate = params.get("returnDate") || "";

  const [flights, setFlights] = useState<Flight[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchFlights() {
      try {
        setLoading(true);
        
        const response = await fetch('http://localhost:5000/api/search-flights', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            origin,
            destination,
            budget,
            departureDate,
            returnDate: returnDate || undefined
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to fetch flights');
        }

        const flightData = await response.json();
        setFlights(flightData);
        setError(null);
      } catch (err) {
        console.error('Error fetching flights:', err);
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
        setFlights([]);
      } finally {
        setLoading(false);
      }
    }

    fetchFlights();
  }, [origin, destination, budget, departureDate, returnDate]);

  return (
    <div className="results-page">
      {/* Cat airplane decorations */}
      <div className="cat-airplane-decoration cat-1" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
      <div className="cat-airplane-decoration cat-2" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
      <div className="cat-airplane-decoration cat-3" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
      <div className="cat-airplane-decoration cat-4" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
      
      <div className="logo-container">
        <img src={catLogo} alt="FareCat Logo" className="cat-logo" />
      </div>
      
      <div className="results-container">
        <div className="header-container">
          <h1 className="destination-title">
            Flights from {origin} to {destination}
          </h1>
          <p className="budget-text">
            Showing flights within your budget of ${budget}
          </p>
        </div>
        
        {loading ? (
          <div className="loading">
            <p>Searching for the purr-fect flights...</p>
            {/* Add a loading spinner or animation here */}
          </div>
        ) : error ? (
          <div className="no-results">
            <p className="text-xl text-gray-700">{error}</p>
            <p className="mt-2 text-gray-500">Try increasing your budget or choosing a different destination.</p>
          </div>
        ) : flights.length > 0 ? (
          <div className="flight-cards-container">
            {flights.map((flight, index) => (
              <div key={index} className="flight-card">
                <div className="airline-header">
                  <h2 className="airline-name">{flight.airline}</h2>
                  <span className="price-tag">${flight.price.toFixed(2)}</span>
                </div>
                
                <div className="flight-times">
                  <div className="departure">
                    <div className="time">{flight.departureTime}</div>
                    <div className="label">Departure</div>
                  </div>
                  
                  <div className="duration">
                    <div>{flight.duration}</div>
                    <div>{flight.stops === 0 ? "Nonstop" : `${flight.stops} stop${flight.stops > 1 ? 's' : ''}`}</div>
                  </div>
                  
                  <div className="arrival">
                    <div className="time">{flight.arrivalTime}</div>
                    <div className="label">Arrival</div>
                  </div>
                </div>
                
                <div className="flight-class">Economy Class</div>
                <div className="flight-type">
                  {flight.stops === 0 ? "Direct Flight" : "Connecting Flight"}
                </div>
                
                <a
                  href={flight.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="book-now-button"
                >
                  Book Now
                </a>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-results">
            <p className="text-xl text-gray-700">No flights found within your budget.</p>
            <p className="mt-2 text-gray-500">Try increasing your budget or choosing a different destination.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Results;