import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles.css";


const Search = () => {
  const [destination, setDestination] = useState("");
  const [budget, setBudget] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (destination && budget) {
      navigate(`/results?destination=${destination}&budget=${budget}`);
    } else {
      alert("Please enter a destination and budget.");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Find Your Flight</h1>
      <input
        type="text"
        placeholder="Enter destination"
        value={destination}
        onChange={(e) => setDestination(e.target.value)}
        className="px-4 py-2 mb-3 border rounded-lg"
      />
      <input
        type="number"
        placeholder="Enter budget ($)"
        value={budget}
        onChange={(e) => setBudget(e.target.value)}
        className="px-4 py-2 mb-3 border rounded-lg"
      />
      <button
        onClick={handleSearch}
        className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
      >
        Search Flights
      </button>
    </div>
  );
};

export default Search;
