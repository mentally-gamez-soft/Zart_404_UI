import reflex as rx

from Zart_404_UI.components.articles.list_articles import (
    article_public_list_component,
)
from Zart_404_UI.routes.navigation_state import NavState


def landing_component() -> rx.Component:
    return rx.vstack(
        rx.heading("Welcome to ZART-404", size="9"),
        rx.button(
            "About Us",
            on_click=NavState.to_about,
            #   bg=rx.color_mode_cond(
            #     light=rx.color(color="tomato",shade=3,alpha=False),
            #     dark=rx.color(color="tomato",shade=8,alpha=False),
            # ), #rx.color(color="tomato",shade=10,alpha=False), #https://www.radix-ui.com/colors #
            #   style={
            #       "cursor":"pointer",
            #       "_hover":{
            #       "bg":rx.color(color="tomato",shade=4,alpha=False)
            #   }}
            # color_scheme="gray"
        ),
        rx.divider(size="4"),
        rx.heading("Latest articles", size="5"),
        article_public_list_component(columns=1, limit=20),
        spacing="5",
        justify="center",
        min_height="85vh",
        align="center",
        id="my-element-test",
    )
