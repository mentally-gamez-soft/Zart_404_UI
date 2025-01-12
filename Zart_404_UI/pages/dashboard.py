import reflex as rx

from Zart_404_UI.components.articles.list_articles import (
    article_public_list_component,
)


def dashboard_component() -> rx.Component:
    return rx.box(
        rx.heading("Welcome back", size="4"),
        rx.divider(margin_top="1em", margin_bottom="1em"),
        article_public_list_component(columns=3, limit=20, spacing=3),
        min_height="85vh",
    )
