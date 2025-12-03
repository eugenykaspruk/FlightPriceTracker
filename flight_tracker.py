import argparse
import sys
import pandas as pd
import numpy as np
import requests
from datetime import date
from typing import List, Dict, Any, Optional

# --- API Configuration ---
RAPIDAPI_KEY = "afee6ff878msh6d6b83e5472fc03p1d7d58jsn7f247cf47cf3"
API_HOST = "google-flights4.p.rapidapi.com"
API_URL = f"https://{API_HOST}/price-graph/for-one-way"


def fetch_flight_prices(origin_id: str, destination_id: str) -> Optional[List[float]]:
    """
    Fetches a list of historical/future flight prices for a route
    from the Google Flights 4 Unofficial API on RapidAPI.

    Args:
        origin_id: The IATA code for the departure city (e.g., KBP).
        destination_id: The IATA code for the arrival city (e.g., WAW).

    Returns:
        A list of float prices, or None if the call fails.
    """
    today_date_str = date.today().isoformat()

    print(f"✈️ Fetching data for route: {origin_id}-{destination_id} starting {today_date_str}...")

    # Your provided API configuration, updated for dynamic IDs and the key
    querystring = {
        "departureId": origin_id,
        "arrivalId": destination_id,
        "departureDate": today_date_str
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,  # Required by RapidAPI
        "x-rapidapi-host": API_HOST
    }

    try:
        response = requests.get(API_URL, headers=headers, params=querystring, timeout=15)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # We need to extract the price for each data point.
        price_points = data.get('data', [])

        # Check if we got any data points
        if not price_points:
            print(
                f"⚠️ API returned successfully, but no price data points were found for {origin_id}-{destination_id}.")
            return None

        # Extract only the prices (as integers/floats)
        prices: List[float] = [float(point.get('price')) for point in price_points if point.get('price') is not None]

        return prices

    except requests.exceptions.RequestException as e:
        print(f"❌ Network/API Error occurred: {e}")
        return None
    except Exception as e:
        print(f"❌ Failed to process API response: {e}")
        return None


def analyze_prices(prices_list: List[float]) -> Dict[str, Any]:
    """
    Computes min, max, mean, and identifies anomalies using the Z-score.
    """
    if not prices_list:
        return {'error': 'No price data available for analysis.'}

    # Use Pandas Series for easy statistical computation
    prices_series = pd.Series(prices_list)

    # 1. Compute min, max, mean, and standard deviation (NumPy/Pandas)
    min_price = prices_series.min()
    max_price = prices_series.max()
    mean_price = prices_series.mean()
    std_dev = prices_series.std()

    if std_dev == 0:
        return {
            'min': min_price,
            'max': max_price,
            'mean': mean_price,
            'anomalies': [],
            'note': 'Standard deviation is zero (all prices are the same).'
        }

    # 2. Find Anomalies (Z-score > 2) using NumPy
    # Z-score formula: Z = np.abs((x - mean) / std)
    z_scores = np.abs((prices_series - mean_price) / std_dev)

    # Identify the actual prices that are anomalies and convert back to list
    anomalies = prices_series[z_scores > 2].tolist()

    return {
        'min': min_price,
        'max': max_price,
        'mean': mean_price,
        'std_dev': std_dev,
        'total_data_points': len(prices_list),
        'anomalies': anomalies
    }


def main():
    """
    Main entry point for the Command Line Interface (CLI) application.
    """
    parser = argparse.ArgumentParser(
        description="Flight Price Tracker: Analyze flight prices for a given route.",
        epilog="Example: python flight_tracker.py --route KBP-WAW"
    )
    # Required argument: --route
    parser.add_argument(
        '--route',
        type=str,
        required=True,
        help="The flight route to analyze (e.g., KBP-WAW). Must use IATA codes (3 letters)."
    )

    args = parser.parse_args()

    try:
        # Split the route into origin and destination
        parts = args.route.upper().split('-')
        if len(parts) != 2 or len(parts[0]) != 3 or len(parts[1]) != 3:
            raise ValueError("Route format invalid.")

        origin, destination = parts[0], parts[1]
    except ValueError:
        print("❌ Error: Route format must be 'ORIGIN-DESTINATION' using 3-letter IATA codes (e.g., KBP-WAW).")
        sys.exit(1)

    # 1. Fetch Data
    prices = fetch_flight_prices(origin, destination)

    if prices is None or not prices:
        print(f"❌ Could not retrieve or parse any price data for {args.route}. Exiting.")
        sys.exit(1)

    # 2. Analyze Data
    results = analyze_prices(prices)

    # 3. Output Results
    print("\n" + "=" * 50)
    print(f"📊 Flight Price Analysis for {origin} -> {destination}")
    print("=" * 50)

    if 'error' in results:
        print(f"Analysis failed: {results['error']}")
    else:
        print(f"Total Prices Analyzed: {results['total_data_points']}")
        print(f"Min Price:             {results['min']:.2f}")
        print(f"Max Price:             {results['max']:.2f}")
        print(f"Average (Mean) Price:  {results['mean']:.2f}")
        print(f"Standard Deviation:    {results['std_dev']:.2f}")

        print("-" * 50)

        anomalies = results['anomalies']
        print(f"Anomalies Found (Z-score > 2): {len(anomalies)}")

        if anomalies:
            print("🚨 ANOMALOUS PRICES:")
            for price in sorted(anomalies, reverse=True):
                print(f"   > {price:.2f}")
        else:
            print("✅ No price anomalies detected.")


if __name__ == "__main__":
    main()