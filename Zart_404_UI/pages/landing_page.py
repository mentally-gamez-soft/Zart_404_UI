import reflex as rx

from Zart_404_UI.articles.list_articles import article_public_list_component
from Zart_404_UI.routes.navigation_state import NavState


def landing_component() -> rx.Component:
    return rx.vstack(
        rx.heading("Welcome to ZART-404", size="9"),
        rx.button("About Us", on_click=NavState.to_about),
        rx.divider(size="4"),
        rx.heading("Latest articles", size="5"),
        article_public_list_component(columns=1, limit=20),
        spacing="5",
        justify="center",
        min_height="85vh",
        align="center",
        id="my-element-test",
    )
