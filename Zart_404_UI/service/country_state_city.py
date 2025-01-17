import requests

from . import request_headers


def get_all_countries():
    url = "https://api.countrystatecity.in/v1/countries"
    response = requests.get(url=url, headers=request_headers)

    return [
        {
            key: value
            for (key, value) in country.items()
            if key in ("name", "iso2")
        }
        for country in response.json()
    ]


def get_cities_of_country(country_iso_2: str):
    url = (
        f"https://api.countrystatecity.in/v1/countries/{country_iso_2}/cities"
    )
    response = requests.get(url=url, headers=request_headers)
    return [city["name"] for city in response.json()]
