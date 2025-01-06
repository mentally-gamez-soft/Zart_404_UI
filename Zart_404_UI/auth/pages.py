import reflex as rx
from reflex_local_auth.pages.login import LoginState, login_form
from reflex_local_auth.pages.registration import RegistrationState

from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.constantes.routes import URLS
from Zart_404_UI.pages.base_page import base_page

from .forms import custom_register_form


def custom_login_page() -> rx.Component:
    return base_page(
        rx.center(
            rx.cond(
                LoginState.is_hydrated,  # type: ignore
                rx.card(login_form()),
            ),
            min_height="85vh",
        )
    )


def custom_register_page() -> rx.Component:
    return base_page(
        rx.center(
            rx.cond(
                RegistrationState.success,
                rx.vstack(
                    rx.text("Registration successful!"),
                ),
                rx.card(custom_register_form()),
            ),
            min_height="85vh",
        )
    )


def logout_confirm_page() -> rx.Component:

    return base_page(
        rx.vstack(
            rx.heading("Confirming logout ?", size="7"),
            rx.link(
                rx.button("No, not yet.", color_scheme="gray"),
                href=URLS["home"],
            ),
            rx.button(
                "Yes, please log me out.",
                on_click=UserSessionState.execute_logout,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
            id="my-element-test",
        ),
    )
