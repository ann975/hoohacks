import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "../styles.css";


interface Flight {
  airline: string;
  price: number;
  link: string;
}

const Results = () => {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const destination = params.get("destination");
  const budget = params.get("budget");

  const [flights, setFlights] = useState<Flight[]>([]);

  useEffect(() => {
    // Mock flight data (replace with actual API call later)
    const mockFlights: Flight[] = [
      { airline: "Delta", price: 250, link: "https://www.delta.com" },
      { airline: "United", price: 300, link: "https://www.united.com" },
      { airline: "Southwest", price: 180, link: "https://www.southwest.com" },
    ];

    const filteredFlights = mockFlights.filter((flight) => flight.price <= Number(budget));
    setFlights(filteredFlights);
  }, [budget]);

  return (
    <div className="p-8 bg-white min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Flights to {destination}</h1>
      {flights.length > 0 ? (
        flights.map((flight, index) => (
          <div key={index} className="p-4 mb-3 border rounded-lg">
            <p className="text-lg font-semibold">{flight.airline}</p>
            <p>Price: ${flight.price}</p>
            <a href={flight.link} target="_blank" rel="noopener noreferrer" className="text-blue-500">
              Book Now
            </a>
          </div>
        ))
      ) : (
        <p>No flights found within your budget.</p>
      )}
    </div>
  );
};

export default Results;
