"""Demo version of flight tracker with sample data."""

import json
from datetime import datetime
import random

from config import (
    ORIGIN_AIRPORT,
    LATIN_AMERICAN_DESTINATIONS,
    CABIN_CLASS,
    SEARCH_MONTH
)


def generate_demo_data():
    """Generate realistic sample flight data."""
    results = []

    # Base prices for different countries (USD)
    base_prices = {
        "Argentina": 3200,
        "Brazil": 2800,
        "Chile": 3400,
        "Colombia": 2600,
        "Mexico": 2400,
        "Peru": 2900,
        "Ecuador": 2700,
        "Uruguay": 3300,
        "Venezuela": 2500,
        "Costa Rica": 2300,
        "Panama": 2200,
        "Guatemala": 2450,
        "Bolivia": 3100,
        "Paraguay": 3250,
    }

    carriers = {
        "EK": "Emirates",
        "QR": "Qatar Airways",
        "TK": "Turkish Airlines",
        "LH": "Lufthansa",
        "AF": "Air France",
        "KL": "KLM",
        "LA": "LATAM",
        "AM": "Aeromexico",
        "CM": "Copa Airlines"
    }

    sample_dates = ["2026-05-01", "2026-05-05", "2026-05-09"]

    for country, airports in LATIN_AMERICAN_DESTINATIONS.items():
        base_price = base_prices[country]

        for airport in airports:
            for date in sample_dates[:2]:  # 2 dates per airport
                # Generate 2-3 offers per date
                for i in range(random.randint(2, 3)):
                    price_variation = random.uniform(0.85, 1.15)
                    price = round(base_price * price_variation, 2)

                    stops = random.choice([0, 1, 1, 2])  # More 1-stop flights

                    # Pick carriers
                    num_carriers = stops + 1
                    flight_carriers = random.sample(list(carriers.keys()), num_carriers)

                    # Duration increases with stops
                    base_duration = random.randint(16, 20)
                    duration_hours = base_duration + (stops * random.randint(2, 4))
                    duration_mins = random.randint(0, 59)

                    results.append({
                        'country': country,
                        'airport': airport,
                        'price': price,
                        'currency': 'USD',
                        'departure_date': date,
                        'departure_time': f"{date}T23:45:00",
                        'arrival_time': f"{date}T{(duration_hours % 24):02d}:{duration_mins:02d}:00",
                        'duration': f"PT{duration_hours}H{duration_mins}M",
                        'stops': stops,
                        'carriers': ', '.join(flight_carriers)
                    })

    return results


def print_summary(results):
    """Print summary of results."""
    print("\n" + "=" * 80)
    print("FLIGHT SEARCH SUMMARY (DEMO DATA)")
    print("=" * 80)

    print(f"\nTotal offers found: {len(results)}")

    # Top 10 cheapest
    print("\n" + "-" * 80)
    print("TOP 10 CHEAPEST BUSINESS CLASS FLIGHTS")
    print("-" * 80)

    sorted_results = sorted(results, key=lambda x: x['price'])

    for flight in sorted_results[:10]:
        print(f"\n{flight['country']} ({flight['airport']})")
        print(f"  Price: {flight['currency']} {flight['price']:.2f}")
        print(f"  Date: {flight['departure_date']}")
        print(f"  Duration: {flight['duration']}")
        print(f"  Stops: {flight['stops']}")
        print(f"  Carrier(s): {flight['carriers']}")

    # Cheapest by country
    print("\n" + "-" * 80)
    print("CHEAPEST FLIGHT TO EACH COUNTRY")
    print("-" * 80)

    country_cheapest = {}
    for flight in results:
        country = flight['country']
        if country not in country_cheapest or flight['price'] < country_cheapest[country]['price']:
            country_cheapest[country] = flight

    sorted_countries = sorted(country_cheapest.items(), key=lambda x: x[1]['price'])

    for country, flight in sorted_countries:
        print(f"{country:20} {flight['airport']:6} {flight['currency']} {flight['price']:10.2f}  ({flight['departure_date']})")

    print("\n" + "=" * 80)


def main():
    """Run demo."""
    print("Dubai to Latin America Business Class Flight Tracker")
    print("=" * 80)
    print("\n🎭 DEMO MODE - Using sample data")
    print("   (To use real data, install dependencies and configure API credentials)\n")

    print(f"Searching business class flights from {ORIGIN_AIRPORT} in May 2026...")
    print(f"Destinations: {sum(len(airports) for airports in LATIN_AMERICAN_DESTINATIONS.values())} airports")
    print("-" * 80)

    # Generate sample data
    results = generate_demo_data()

    # Show some search progress
    for country, airports in list(LATIN_AMERICAN_DESTINATIONS.items())[:5]:
        print(f"\nSearching {country}...")
        for airport in airports[:1]:
            print(f"  Airport: {airport}")
            print(f"    2026-05-01: Found 3 offers")

    print(f"\n... (searching {len(LATIN_AMERICAN_DESTINATIONS) - 5} more countries)")

    # Print summary
    print_summary(results)

    # Save results
    with open('flight_results_demo.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Demo results saved to flight_results_demo.json")
    print(f"\n💡 This is sample data. For real flight prices:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Get API credentials from https://developers.amadeus.com/")
    print("   3. Configure .env file")
    print("   4. Run: python flight_tracker.py")


if __name__ == '__main__':
    main()
