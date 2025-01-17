import requests

from . import request_headers


def get_all_countries():
    url = "https://api.countrystatecity.in/v1/countries"
    response = requests.get(url=url, headers=request_headers)
    print(response.json())


def get_cities_of_country(country_iso_2: str):
    url = (
        f"https://api.countrystatecity.in/v1/countries/{country_iso_2}/cities"
    )
    response = requests.get(url=url, headers=request_headers)
    print(response.json())
