import { Link } from "react-router-dom";
import "../styles.css";


const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-blue-100">
      <h1 className="text-3xl font-bold mb-6">Welcome to Flight Price Tracker</h1>
      <Link to="/search">
        <button className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
          Start Searching Flights
        </button>
      </Link>
    </div>
  );
};

export default Home;
