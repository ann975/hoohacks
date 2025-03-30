import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "../styles.css";
import "./Results.css";
import catAirplaneGif from "./cat-airplane.gif"; // Import the GIF
import catLogo from "./cat-logo.jpg"; // Import the cat logo

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
  const destination = params.get("destination") || "San Diego";
  const budget = params.get("budget") || "400";

  const [flights, setFlights] = useState<Flight[]>([]);

  useEffect(() => {
    // Mock flight data (replace with actual API call later)
    const mockFlights: Flight[] = [
      {
        airline: "Delta",
        price: 250,
        link: "https://www.delta.com",
        departureTime: "08:30 AM",
        arrivalTime: "11:45 AM",
        duration: "3h 15m",
        stops: 0
      },
      {
        airline: "United",
        price: 300,
        link: "https://www.united.com",
        departureTime: "10:15 AM",
        arrivalTime: "01:30 PM",
        duration: "3h 15m",
        stops: 0
      },
      {
        airline: "Southwest",
        price: 180,
        link: "https://www.southwest.com",
        departureTime: "07:45 AM",
        arrivalTime: "11:20 AM",
        duration: "3h 35m",
        stops: 1
      },
    ];

    const filteredFlights = mockFlights.filter(
      (flight) => flight.price <= Number(budget)
    );
    setFlights(filteredFlights);
  }, [budget]);

  return (
    <div className="results-page">
      {/* Cat airplane decorations */}
      <div className="cat-airplane-decoration cat-1" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
      <div className="cat-airplane-decoration cat-2" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
      <div className="cat-airplane-decoration cat-3" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
      <div className="cat-airplane-decoration cat-4" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
      
      <div className="results-container">
        <div className="header-container">
          <h1 className="destination-title">
            Flights to {destination}
          </h1>
          <p className="budget-text">
            Showing flights within your budget of ${budget}
          </p>
        </div>
        
        {flights.length > 0 ? (
          <div className="flight-cards-container">
            {flights.map((flight, index) => (
              <div key={index} className="flight-card">
                <div className="airline-header">
                  <h2 className="airline-name">{flight.airline}</h2>
                  <span className="price-tag">${flight.price}</span>
                </div>
                
                <div className="flight-times">
                  <div className="departure">
                    <div className="time">{flight.departureTime}</div>
                    <div className="label">Departure</div>
                  </div>
                  
                  <div className="duration">
                    <div>{flight.duration}</div>
                    <div>{flight.stops === 0 ? "Nonstop" : `${flight.stops} stop`}</div>
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
      
      <div className="logo-container">
        <img src={catLogo} alt="FareCat Logo" className="cat-logo" />
      </div>
    </div>
  );
};

export default Results;