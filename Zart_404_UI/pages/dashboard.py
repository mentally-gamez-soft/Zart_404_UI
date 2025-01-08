import reflex as rx

from .sidebar import sidebar


def base_dashboard_page(child_component: rx.Component) -> rx.Component:
    return rx.fragment(
        rx.hstack(
            sidebar(),
            rx.box(
                child_component,
                rx.logo(),
                # bg=rx.color("accent", 3),
                padding="1em",
                width="100%",
            ),
        ),
        # rx.color_mode.button(position="bottom-left", id="color-mode"),
    )
