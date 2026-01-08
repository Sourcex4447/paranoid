"""Configuration for flight price tracker."""

# Origin airport
ORIGIN_AIRPORT = "DXB"  # Dubai International Airport

# Latin American countries and their major airports
LATIN_AMERICAN_DESTINATIONS = {
    "Argentina": ["EZE", "AEP"],  # Buenos Aires
    "Brazil": ["GRU", "GIG", "BSB"],  # São Paulo, Rio de Janeiro, Brasília
    "Chile": ["SCL"],  # Santiago
    "Colombia": ["BOG", "MDE"],  # Bogotá, Medellín
    "Mexico": ["MEX", "CUN", "GDL"],  # Mexico City, Cancún, Guadalajara
    "Peru": ["LIM"],  # Lima
    "Ecuador": ["UIO", "GYE"],  # Quito, Guayaquil
    "Uruguay": ["MVD"],  # Montevideo
    "Venezuela": ["CCS"],  # Caracas
    "Costa Rica": ["SJO"],  # San José
    "Panama": ["PTY"],  # Panama City
    "Guatemala": ["GUA"],  # Guatemala City
    "Bolivia": ["LPB", "VVI"],  # La Paz, Santa Cruz
    "Paraguay": ["ASU"],  # Asunción
}

# Travel class
CABIN_CLASS = "BUSINESS"

# Month to search (May)
SEARCH_MONTH = 5

# Number of days to stay (flexible - can be configured)
DEFAULT_TRIP_DURATION = 7

# Maximum number of results per destination
MAX_RESULTS_PER_DESTINATION = 5
