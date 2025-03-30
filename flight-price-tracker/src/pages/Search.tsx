import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles.css";
import "./Search.css";
import catLogo from "./cat-logo.jpg";

const Search = () => {
  const [origin, setOrigin] = useState("DCA");
  const [destination, setDestination] = useState("");
  const [budget, setBudget] = useState("");
  const [departureDate, setDepartureDate] = useState("");
  const [returnDate, setReturnDate] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (destination && budget && origin && departureDate) {
      navigate(`/results?origin=${origin}&destination=${destination}&budget=${budget}&departureDate=${departureDate}&returnDate=${returnDate}`);
    } else {
      alert("Please fill in all required fields.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-pink-300 via-purple-400 to-blue-500 p-4 relative">
      {/* Cat airplane decorations */}
      <div className="cat-airplane cat-1"></div>
      <div className="cat-airplane cat-2"></div>
      <div className="cat-airplane cat-3"></div>
      <div className="cat-airplane cat-4"></div>
      
      {/* Cat Logo */}
      <div className="cat-logo-container">
        <img src={catLogo} alt="FareCat Logo" className="cat-logo" />
      </div>
      
      <div className="search-container max-w-md w-full text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-8 text-white">Find Your Flight</h1>
        
        <div className="input-group">
          <input
            type="text"
            placeholder="Enter origin airport code (e.g., DCA)"
            value={origin}
            onChange={(e) => setOrigin(e.target.value.toUpperCase())}
            className="search-input"
          />
        </div>
        
        <div className="input-group">
          <input
            type="text"
            placeholder="Enter destination airport code"
            value={destination}
            onChange={(e) => setDestination(e.target.value.toUpperCase())}
            className="search-input"
          />
        </div>
        
        <div className="input-group">
          <input
            type="date"
            placeholder="Departure date"
            value={departureDate}
            onChange={(e) => setDepartureDate(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="input-group">
          <input
            type="date"
            placeholder="Return date (optional)"
            value={returnDate}
            onChange={(e) => setReturnDate(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="input-group">
          <input
            type="number"
            placeholder="Enter budget ($)"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            className="search-input"
          />
        </div>
        
        <button
          onClick={handleSearch}
          className="search-button"
        >
          Search Flights
        </button>
      </div>
    </div>
  );
};

export default Search;