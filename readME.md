# **🪙 Crypto Price Scraper & API**

This project is a full-stack Python application that scrapes real-time cryptocurrency data from **CoinMarketCap**, stores the historical price data in a local **MongoDB** database, and serves that data via a **Flask REST API**.

## **📋 Features**

* **Web Scraper (scraper.py):** Uses Selenium to automate Google Chrome, navigating to CoinMarketCap pages for a specific list of cryptocurrencies (Bitcoin, Ethereum, Solana, etc.) to extract prices and 24h percentage changes.  
* **Database Integration:** Stores scraping results (Name, Price, Change, Timestamp) in a local MongoDB collection (proiect\_crypto).  
* **REST API (app.py):** A lightweight Flask server that exposes an endpoint to retrieve the stored data in JSON format.

## **⚙️ Prerequisites**

Before running the project, ensure you have the following installed:

1. **Python 3.x**  
2. **Google Chrome Browser** (required for Selenium automation).  
3. **MongoDB Community Server** (must be installed and running locally on port 27017).

## **🛠️ Installation & Setup**

Follow these steps to set up your development environment.

### **1\. Create and Activate a Virtual Environment**

It is recommended to run this project in a virtual environment to manage dependencies.

**Windows (PowerShell):**

\# Create the environment  
python \-m venv venv

\# Set execution policy (required if scripts are blocked)  
Set-ExecutionPolicy Unrestricted \-Scope Process

\# Activate the environment  
.\\venv\\Scripts\\activate

**Mac/Linux:**

python3 \-m venv venv  
source venv/bin/activate

### **2\. Install Dependencies**

Install the required Python libraries using pip:

pip install selenium webdriver-manager beautifulsoup4 lxml flask pymongo requests

## **🚀 Usage**

### **Step 1: Start MongoDB**

Ensure your local MongoDB instance is running. You can usually start it via your system services or by running mongod in your terminal.

### **Step 2: Run the Scraper**

Run the scraper script to fetch data from the web and populate your database.

python scraper.py

* *Note: This will open a Chrome window and cycle through the list of coins defined in the script. Do not close the window manually; the script will close it upon completion.*

### **Step 3: Start the API Server**

Once the data is populated, start the Flask application.

python app.py

* The server will start at http://127.0.0.1:5000/.

## **📡 API Documentation**

### **Get All Prices**

Retrieves the history of scraped prices from the database.

* **Endpoint:** /api/preturi  
* **Method:** GET  
* **URL:** http://127.0.0.1:5000/api/preturi

**Example Response:**

\[  
  {  
    "nume\_moneda": "Bitcoin",  
    "pret": "$98,000.00",  
    "modificare\_24h": "+5.20%",  
    "timestamp": "Fri, 12 Dec 2025 10:00:00 GMT"  
  },  
  {  
    "nume\_moneda": "Ethereum",  
    "pret": "$2,800.00",  
    "modificare\_24h": "-1.50%",  
    "timestamp": "Fri, 12 Dec 2025 10:00:00 GMT"  
  }  
\]

## **📂 Project Structure**

| File | Description |
| :---- | :---- |
| scraper.py | Main script using Selenium to scrape CoinMarketCap and insert data into MongoDB. |
| app.py | Flask application serving the API endpoints. |
| venv/ | (Generated) Virtual environment folder containing dependencies. |

