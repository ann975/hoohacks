  import { Link } from "react-router-dom";
  import "../styles.css";
  import "./Home.css";
  import catAirplaneGif from "./cat-airplane.gif"; // Import the GIF
  import catLogo from "./cat-logo.jpg"; // Import the logo image


  const Home = () => {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-50 to-blue-200 p-4 relative">
        {/* Cat airplane decorations with inline style as backup */}
        <div className="cat-airplane cat-1" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
        <div className="cat-airplane cat-2" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
        <div className="cat-airplane cat-3" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
        <div className="cat-airplane cat-4" style={{backgroundImage: `url(${catAirplaneGif})`}}></div>
        
        {/* Add the logo container here */}
      <div className="cat-logo-container">
        <img src={catLogo} alt="FareCat Logo" className="cat-logo" />
      </div>

        <div className="hero-container max-w-3xl text-center">
          <div className="feature-tag">Flight Price Tracking</div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="logo-text">Welcome to</span>{" "}
            <span className="logo-text">FareCat!</span>
          </h1>
          
          <p className="text-lg text-gray-700 mb-8 max-w-xl mx-auto">
            Find the best deals on flights and track price changes to book at the perfect time.
          </p>
          
          <div className="space-y-4 md:flex md:space-y-0 md:space-x-4 md:justify-center">
            <Link to="/search">
              <button 
                className="cta-button-primary w-full md:w-auto px-8 py-4 rounded-lg hover:bg-blue-700 transition-colors duration-300 shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                aria-label="Start searching for flights"
              >
                Start Searching Flights
              </button>
            </Link>
            
            <Link to="/how-it-works">
              <button 
                className="cta-button-secondary w-full md:w-auto px-8 py-4 rounded-lg hover:bg-blue-50 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                aria-label="Learn how flight price tracking works"
              >
                How It Works
              </button>
            </Link>
          </div>
        </div>
        
        <div className="mt-16 text-center">
          <p className="text-sm text-gray-600">
            Track prices across multiple airlines and get notified when prices drop
          </p>
        </div>
      </div>
    );
  };

  export default Home;