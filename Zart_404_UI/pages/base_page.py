import reflex as rx

from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.pages.shared.navbar import NAVBAR_TITLE, navbar

from .dashboard import base_dashboard_page


def default_navbar(child_component: rx.Component) -> rx.Component:
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


def base_page(child_component: rx.Component) -> rx.Component:
    is_logged_in = True

    return rx.cond(
        UserSessionState.is_authenticated,
        base_dashboard_page(child_component),
        default_navbar(child_component),
    )
