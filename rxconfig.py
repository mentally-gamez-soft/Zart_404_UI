import os

import reflex as rx
from dotenv import load_dotenv

load_dotenv()

config = rx.Config(
    app_name="Zart_404_UI",
    bd_url="sqlite:///Zart_404_UI.db",
    COUNTRIES_CITIES_API_KEY=os.getenv("COUNTRIES_CITIES_API_KEY"),
)
