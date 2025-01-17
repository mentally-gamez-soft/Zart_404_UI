from rxconfig import config

request_headers = {"X-CSCAPI-KEY": config.COUNTRIES_CITIES_API_KEY}

from .country_state_city import get_all_countries, get_cities_of_country

__all__ = ["get_all_countries", "get_cities_of_country"]
