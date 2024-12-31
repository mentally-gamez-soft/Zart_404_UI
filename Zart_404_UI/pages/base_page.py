import reflex as rx

from Zart_404_UI.pages.shared.navbar import NAVBAR_TITLE, navbar


def base_page(child_component: rx.Component) -> rx.Component:
    return rx.fragment(
        navbar(title=NAVBAR_TITLE),
        rx.box(
            child_component,
            # bg=rx.color("accent", 3),
            padding="1em",
            width="100%",
        ),
        rx.logo(),
        rx.color_mode.button(position="bottom-left", id="color-mode"),
        id="base-page",
    )
