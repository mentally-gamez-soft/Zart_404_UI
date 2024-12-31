"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from Zart_404_UI.pages.base_page import base_page


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    # Welcome Page (Index)

    return base_page(
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
            id="my-element-test",
        ),
    )


app = rx.App()
app.add_page(index)
