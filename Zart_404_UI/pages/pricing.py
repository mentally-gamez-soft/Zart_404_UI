import reflex as rx

from Zart_404_UI.pages.base_page import base_page


def pricing_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Pricing", size="9"),
            rx.text(
                "Our pricing",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            id="about-page",
        ),
    )
