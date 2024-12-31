import reflex as rx

from Zart_404_UI.constantes import URLS
from Zart_404_UI.pages.base_page import base_page


@rx.page(route=URLS["contact"])
def contact_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Contact Us", size="9"),
            rx.text(
                "This is us",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            id="about-page",
        ),
    )
