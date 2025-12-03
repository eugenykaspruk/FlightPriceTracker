# ✈️ Flight Price Tracker

A robust Python console application (CLI) designed to fetch historical or indicative flight price data for a specified route, perform statistical analysis, and identify statistical outliers (anomalies) in the pricing.

## 🚀 Project Description
This project meets the requirements of a large course assignment by demonstrating:
* A working external API network call (`requests`).
* Data processing using the **Pandas** and **NumPy** libraries.
* A professional, containerized deployment using **Docker**.

### Analysis Features
* **Route:** Accepts IATA codes for one-way routes (e.g., KBP-WAW).
* **Statistics:** Computes the minimum, maximum, and mean (average) price.
* **Anomaly Detection:** Identifies prices that are statistically significant outliers using the Z-score method. An anomaly is flagged if its Z-score is greater than 2.

## 🔗 API Used
* **API Name:** Google Flights 4 Unofficial API (via RapidAPI)
* **Link to Docs:** https://google-flights4.p.rapidapi.com/price-graph/for-one-way

## 🔧 How to Run Locally

### Prerequisites
* Python 3.8+
* `pip` (Python package installer)

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/eugenykaspruk/flight-price-tracker.git
    cd flight-price-tracker
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set API Key:**
    Edit the `flight_tracker.py` file and replace `"YOUR_RAPIDAPI_KEY_HERE"` with your actual `x-rapidapi-key`.

4.  **Example CLI Command:**
    Run the application, passing the route as an argument using 3-letter IATA codes.
    ```bash
    python flight_tracker.py --route JFK-LOS
    ```

## 🐳 How to Run via Docker

This project includes a `Dockerfile` for seamless deployment.

### 1. Build the Docker Image
*(Replace `yourusername` with your Docker Hub username)*
```bash
docker build -t yourusername/flight-tracker:latest .