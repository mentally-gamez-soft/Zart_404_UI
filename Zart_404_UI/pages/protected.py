import reflex as rx
import reflex_local_auth

from Zart_404_UI.pages.base_page import base_page


@reflex_local_auth.require_login
def protected_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Protected page", size="9"),
            rx.text(
                "This is us",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )
