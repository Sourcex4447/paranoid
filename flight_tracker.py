"""Flight price tracker for finding cheapest business class tickets from Dubai to Latin America."""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
from dotenv import load_dotenv
from amadeus import Client, ResponseError
import pandas as pd

from config import (
    ORIGIN_AIRPORT,
    LATIN_AMERICAN_DESTINATIONS,
    CABIN_CLASS,
    SEARCH_MONTH,
    DEFAULT_TRIP_DURATION,
    MAX_RESULTS_PER_DESTINATION
)


class FlightPriceTracker:
    """Tracks flight prices from Dubai to Latin American destinations."""

    def __init__(self):
        """Initialize the flight tracker with Amadeus API credentials."""
        load_dotenv()

        api_key = os.getenv('AMADEUS_API_KEY')
        api_secret = os.getenv('AMADEUS_API_SECRET')

        if not api_key or not api_secret:
            raise ValueError(
                "Missing Amadeus API credentials. "
                "Please set AMADEUS_API_KEY and AMADEUS_API_SECRET in .env file"
            )

        self.client = Client(
            client_id=api_key,
            client_secret=api_secret
        )

        self.results = []

    def get_may_dates(self, year: Optional[int] = None) -> List[str]:
        """Generate a list of dates in May for the search.

        Args:
            year: The year to search. Defaults to next May (current year if before May, next year if after).

        Returns:
            List of date strings in YYYY-MM-DD format.
        """
        if year is None:
            current_date = datetime.now()
            if current_date.month >= 5:
                year = current_date.year + 1
            else:
                year = current_date.year

        # Sample dates throughout May (every 3-4 days to reduce API calls)
        sample_dates = []
        for day in [1, 5, 9, 13, 17, 21, 25, 29]:
            date_str = f"{year}-05-{day:02d}"
            sample_dates.append(date_str)

        return sample_dates

    def search_flights(
        self,
        destination: str,
        departure_date: str,
        adults: int = 1,
        max_results: int = 5
    ) -> List[Dict]:
        """Search for flights to a specific destination.

        Args:
            destination: IATA airport code
            departure_date: Date in YYYY-MM-DD format
            adults: Number of adult passengers
            max_results: Maximum number of results to return

        Returns:
            List of flight offers
        """
        try:
            response = self.client.shopping.flight_offers_search.get(
                originLocationCode=ORIGIN_AIRPORT,
                destinationLocationCode=destination,
                departureDate=departure_date,
                adults=adults,
                travelClass=CABIN_CLASS,
                max=max_results
            )

            return response.data if response.data else []

        except ResponseError as error:
            print(f"Error searching flights to {destination} on {departure_date}: {error}")
            return []

    def search_all_destinations(self, year: Optional[int] = None) -> List[Dict]:
        """Search flights to all Latin American destinations.

        Args:
            year: Year to search May dates for

        Returns:
            List of all flight results with metadata
        """
        may_dates = self.get_may_dates(year)
        all_results = []

        print(f"Searching business class flights from {ORIGIN_AIRPORT} in May {may_dates[0][:4]}...")
        print(f"Destinations: {sum(len(airports) for airports in LATIN_AMERICAN_DESTINATIONS.values())} airports")
        print("-" * 80)

        for country, airports in LATIN_AMERICAN_DESTINATIONS.items():
            print(f"\nSearching {country}...")

            for airport in airports:
                print(f"  Airport: {airport}")

                # Search a few sample dates in May
                for date in may_dates[:3]:  # Search first 3 sample dates to limit API calls
                    offers = self.search_flights(
                        destination=airport,
                        departure_date=date,
                        max_results=MAX_RESULTS_PER_DESTINATION
                    )

                    for offer in offers:
                        flight_data = self._parse_flight_offer(offer, country, airport)
                        all_results.append(flight_data)

                    if offers:
                        print(f"    {date}: Found {len(offers)} offers")

        self.results = all_results
        return all_results

    def _parse_flight_offer(self, offer: Dict, country: str, airport: str) -> Dict:
        """Parse flight offer data into a structured format.

        Args:
            offer: Raw flight offer from Amadeus API
            country: Country name
            airport: Airport code

        Returns:
            Parsed flight data dictionary
        """
        price = offer.get('price', {})
        itineraries = offer.get('itineraries', [])

        # Get outbound flight details
        outbound = itineraries[0] if itineraries else {}
        segments = outbound.get('segments', [])

        departure_time = segments[0].get('departure', {}).get('at', '') if segments else ''
        arrival_time = segments[-1].get('arrival', {}).get('at', '') if segments else ''

        # Calculate total duration
        duration = outbound.get('duration', 'N/A')

        # Count stops
        stops = len(segments) - 1

        # Get carriers
        carriers = list(set([
            seg.get('carrierCode', '') for seg in segments
        ]))

        return {
            'country': country,
            'airport': airport,
            'price': float(price.get('total', 0)),
            'currency': price.get('currency', 'USD'),
            'departure_date': departure_time[:10] if departure_time else '',
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'duration': duration,
            'stops': stops,
            'carriers': ', '.join(carriers),
            'booking_link': f"Offer ID: {offer.get('id', 'N/A')}"
        }

    def get_cheapest_flights(self, top_n: int = 10) -> pd.DataFrame:
        """Get the cheapest flights from all results.

        Args:
            top_n: Number of cheapest flights to return

        Returns:
            DataFrame with cheapest flights sorted by price
        """
        if not self.results:
            return pd.DataFrame()

        df = pd.DataFrame(self.results)
        df_sorted = df.sort_values('price').head(top_n)

        return df_sorted

    def get_cheapest_by_country(self) -> pd.DataFrame:
        """Get the cheapest flight to each country.

        Returns:
            DataFrame with cheapest flight per country
        """
        if not self.results:
            return pd.DataFrame()

        df = pd.DataFrame(self.results)
        df_cheapest = df.loc[df.groupby('country')['price'].idxmin()]
        df_sorted = df_cheapest.sort_values('price')

        return df_sorted

    def save_results(self, filename: str = 'flight_results.json'):
        """Save all results to a JSON file.

        Args:
            filename: Output filename
        """
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\nResults saved to {filename}")

    def save_report(self, filename: str = 'flight_report.csv'):
        """Save a detailed report to CSV.

        Args:
            filename: Output filename
        """
        if not self.results:
            print("No results to save")
            return

        df = pd.DataFrame(self.results)
        df_sorted = df.sort_values('price')
        df_sorted.to_csv(filename, index=False)

        print(f"Report saved to {filename}")

    def print_summary(self):
        """Print a summary of the search results."""
        if not self.results:
            print("No results found")
            return

        print("\n" + "=" * 80)
        print("FLIGHT SEARCH SUMMARY")
        print("=" * 80)

        print(f"\nTotal offers found: {len(self.results)}")

        # Overall cheapest
        print("\n" + "-" * 80)
        print("TOP 10 CHEAPEST BUSINESS CLASS FLIGHTS")
        print("-" * 80)

        cheapest = self.get_cheapest_flights(10)
        if not cheapest.empty:
            for idx, row in cheapest.iterrows():
                print(f"\n{row['country']} ({row['airport']})")
                print(f"  Price: {row['currency']} {row['price']:.2f}")
                print(f"  Date: {row['departure_date']}")
                print(f"  Duration: {row['duration']}")
                print(f"  Stops: {row['stops']}")
                print(f"  Carrier(s): {row['carriers']}")

        # Cheapest by country
        print("\n" + "-" * 80)
        print("CHEAPEST FLIGHT TO EACH COUNTRY")
        print("-" * 80)

        by_country = self.get_cheapest_by_country()
        if not by_country.empty:
            for idx, row in by_country.iterrows():
                print(f"{row['country']:20} {row['airport']:6} {row['currency']} {row['price']:10.2f}  ({row['departure_date']})")

        print("\n" + "=" * 80)


def main():
    """Main function to run the flight tracker."""
    print("Dubai to Latin America Business Class Flight Tracker")
    print("=" * 80)

    try:
        tracker = FlightPriceTracker()

        # Search all destinations
        tracker.search_all_destinations()

        # Print summary
        tracker.print_summary()

        # Save results
        tracker.save_results('flight_results.json')
        tracker.save_report('flight_report.csv')

        print("\n✓ Search complete!")

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
