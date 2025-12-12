🪙 Crypto Price Scraper & APIThis project is a full-stack Python application that scrapes real-time cryptocurrency data from CoinMarketCap, stores the historical price data in a local MongoDB database, and serves that data via a Flask REST API.📋 FeaturesWeb Scraper (scraper.py): Uses Selenium to automate Google Chrome, navigating to CoinMarketCap pages for a specific list of cryptocurrencies (Bitcoin, Ethereum, Solana, etc.) to extract prices and 24h percentage changes.Database Integration: Stores scraping results (Name, Price, Change, Timestamp) in a local MongoDB collection (proiect_crypto).REST API (app.py): A lightweight Flask server that exposes an endpoint to retrieve the stored data in JSON format.⚙️ PrerequisitesBefore running the project, ensure you have the following installed:Python 3.xGoogle Chrome Browser (required for Selenium automation).MongoDB Community Server (must be installed and running locally on port 27017).🛠️ Installation & SetupFollow these steps to set up your development environment.1. Create and Activate a Virtual EnvironmentIt is recommended to run this project in a virtual environment to manage dependencies.Windows (PowerShell):# Create the environment
python -m venv venv

# Set execution policy (required if scripts are blocked)
Set-ExecutionPolicy Unrestricted -Scope Process

# Activate the environment
.\venv\Scripts\activate
Mac/Linux:python3 -m venv venv
source venv/bin/activate
2. Install DependenciesInstall the required Python libraries using pip:pip install selenium webdriver-manager beautifulsoup4 lxml flask pymongo requests
🚀 UsageStep 1: Start MongoDBEnsure your local MongoDB instance is running. You can usually start it via your system services or by running mongod in your terminal.Step 2: Run the ScraperRun the scraper script to fetch data from the web and populate your database.python scraper.py
Note: This will open a Chrome window and cycle through the list of coins defined in the script. Do not close the window manually; the script will close it upon completion.Step 3: Start the API ServerOnce the data is populated, start the Flask application.python app.py
The server will start at http://127.0.0.1:5000/.📡 API DocumentationGet All PricesRetrieves the history of scraped prices from the database.Endpoint: /api/preturiMethod: GETURL: http://127.0.0.1:5000/api/preturiExample Response:[
  {
    "nume_moneda": "Bitcoin",
    "pret": "$98,000.00",
    "modificare_24h": "+5.20%",
    "timestamp": "Fri, 12 Dec 2025 10:00:00 GMT"
  },
  {
    "nume_moneda": "Ethereum",
    "pret": "$2,800.00",
    "modificare_24h": "-1.50%",
    "timestamp": "Fri, 12 Dec 2025 10:00:00 GMT"
  }
]
📂 Project StructureFileDescriptionscraper.pyMain script using Selenium to scrape CoinMarketCap and insert data into MongoDB.app.pyFlask application serving the API endpoints.venv/(Generated) Virtual environment folder containing dependencies.