# Flight Price Tracker: Dubai to Latin America

A Python-based flight price tracker that finds the cheapest business class tickets from Dubai to Latin American countries in May.

## Features

- 🌎 Searches **14 Latin American countries** and **28+ major airports**
- 💼 Filters for **business class** tickets only
- 📅 Focuses on **May** travel dates
- 💰 Finds and ranks the **cheapest options**
- 📊 Generates detailed reports in JSON and CSV formats
- 🔄 Uses the **Amadeus Flight API** for real-time pricing

## Supported Destinations

The tracker searches flights to major airports in:

- 🇦🇷 Argentina (Buenos Aires)
- 🇧🇷 Brazil (São Paulo, Rio de Janeiro, Brasília)
- 🇨🇱 Chile (Santiago)
- 🇨🇴 Colombia (Bogotá, Medellín)
- 🇲🇽 Mexico (Mexico City, Cancún, Guadalajara)
- 🇵🇪 Peru (Lima)
- 🇪🇨 Ecuador (Quito, Guayaquil)
- 🇺🇾 Uruguay (Montevideo)
- 🇻🇪 Venezuela (Caracas)
- 🇨🇷 Costa Rica (San José)
- 🇵🇦 Panama (Panama City)
- 🇬🇹 Guatemala (Guatemala City)
- 🇧🇴 Bolivia (La Paz, Santa Cruz)
- 🇵🇾 Paraguay (Asunción)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Amadeus API Credentials

1. Sign up for a free account at [Amadeus for Developers](https://developers.amadeus.com/)
2. Create a new app in your dashboard
3. Copy your API Key and API Secret

### 3. Configure Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```
AMADEUS_API_KEY=your_api_key_here
AMADEUS_API_SECRET=your_api_secret_here
```

## Usage

### Run the Tracker

```bash
python flight_tracker.py
```

The tracker will:
1. Search for business class flights from Dubai (DXB) to all Latin American destinations
2. Sample multiple dates throughout May
3. Display results in the console
4. Generate two output files:
   - `flight_results.json` - Complete data in JSON format
   - `flight_report.csv` - Spreadsheet-friendly report

### Customize Search Parameters

Edit `config.py` to customize:

- `ORIGIN_AIRPORT` - Change departure city (default: Dubai/DXB)
- `CABIN_CLASS` - Change travel class (default: BUSINESS)
- `SEARCH_MONTH` - Change search month (default: 5 for May)
- `DEFAULT_TRIP_DURATION` - Adjust trip length
- `LATIN_AMERICAN_DESTINATIONS` - Add/remove airports

## Output

### Console Output

The tracker displays:
- **Top 10 cheapest flights** overall
- **Cheapest flight to each country**
- Price, date, duration, stops, and carrier information

### Generated Files

**flight_results.json**: Complete flight data
```json
[
  {
    "country": "Mexico",
    "airport": "MEX",
    "price": 2450.00,
    "currency": "USD",
    "departure_date": "2026-05-01",
    "duration": "PT18H30M",
    "stops": 1,
    "carriers": "EK, AM"
  }
]
```

**flight_report.csv**: Spreadsheet with all results sorted by price

## API Rate Limits

The free tier of Amadeus API includes:
- **1,000 free API calls per month**
- Rate limits apply

The tracker is optimized to minimize API calls by:
- Sampling key dates in May (not every day)
- Limiting results per destination

## Requirements

- Python 3.8+
- Internet connection
- Amadeus API credentials (free tier available)

## Dependencies

- `amadeus` - Amadeus flight API client
- `requests` - HTTP library
- `python-dotenv` - Environment variable management
- `pandas` - Data analysis and reporting
- `python-dateutil` - Date utilities

## Troubleshooting

### "Missing Amadeus API credentials" error
- Ensure `.env` file exists with valid credentials
- Check that variable names match exactly: `AMADEUS_API_KEY` and `AMADEUS_API_SECRET`

### No results found
- Some routes may not have business class availability
- Try adjusting dates or destinations in `config.py`
- Check API quota hasn't been exceeded

### API errors
- Verify credentials are correct
- Check internet connection
- Ensure API quota hasn't been exceeded at [Amadeus Dashboard](https://developers.amadeus.com/)

## License

MIT License - Feel free to modify and use for your travel planning needs!

## Contributing

Contributions welcome! Feel free to:
- Add more destinations
- Improve search algorithms
- Add additional APIs
- Enhance reporting features

---

**Happy travels!** ✈️🌎
