"""Test script to validate the tracker without making API calls."""

import sys
from datetime import datetime
from config import (
    ORIGIN_AIRPORT,
    LATIN_AMERICAN_DESTINATIONS,
    CABIN_CLASS,
    SEARCH_MONTH
)


def test_configuration():
    """Test that configuration is properly set up."""
    print("Testing configuration...")

    # Test origin
    assert ORIGIN_AIRPORT == "DXB", f"Expected DXB, got {ORIGIN_AIRPORT}"
    print(f"✓ Origin airport: {ORIGIN_AIRPORT}")

    # Test destinations
    total_airports = sum(len(airports) for airports in LATIN_AMERICAN_DESTINATIONS.values())
    print(f"✓ Countries: {len(LATIN_AMERICAN_DESTINATIONS)}")
    print(f"✓ Total airports: {total_airports}")

    # Test cabin class
    assert CABIN_CLASS == "BUSINESS", f"Expected BUSINESS, got {CABIN_CLASS}"
    print(f"✓ Cabin class: {CABIN_CLASS}")

    # Test month
    assert SEARCH_MONTH == 5, f"Expected 5 (May), got {SEARCH_MONTH}"
    print(f"✓ Search month: {SEARCH_MONTH} (May)")

    print("\n✓ Configuration tests passed!\n")


def test_date_generation():
    """Test date generation logic."""
    print("Testing date generation...")

    from flight_tracker import FlightPriceTracker

    # Create a mock tracker (won't connect to API)
    class MockTracker(FlightPriceTracker):
        def __init__(self):
            # Skip API initialization
            self.results = []

    tracker = MockTracker()
    dates = tracker.get_may_dates(2026)

    print(f"Generated {len(dates)} sample dates in May 2026:")
    for date in dates:
        print(f"  - {date}")

    # Verify all dates are in May
    for date in dates:
        month = int(date.split('-')[1])
        assert month == 5, f"Expected month 5, got {month} in {date}"

    print("\n✓ Date generation tests passed!\n")


def test_destinations():
    """Test that all destinations are valid."""
    print("Testing destinations...")

    for country, airports in LATIN_AMERICAN_DESTINATIONS.items():
        print(f"  {country:20} → {', '.join(airports)}")
        for airport in airports:
            assert len(airport) == 3, f"Invalid airport code: {airport}"
            assert airport.isupper(), f"Airport code must be uppercase: {airport}"

    print(f"\n✓ All {sum(len(a) for a in LATIN_AMERICAN_DESTINATIONS.values())} airport codes validated!\n")


def main():
    """Run all tests."""
    print("=" * 80)
    print("FLIGHT TRACKER VALIDATION TESTS")
    print("=" * 80)
    print()

    try:
        test_configuration()
        test_date_generation()
        test_destinations()

        print("=" * 80)
        print("✓ ALL TESTS PASSED!")
        print("=" * 80)
        print()
        print("The tracker is ready to use. To run with real API calls:")
        print("  1. Set up your .env file with Amadeus API credentials")
        print("  2. Run: python flight_tracker.py")
        print()

        return 0

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
