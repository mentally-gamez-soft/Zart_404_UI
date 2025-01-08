import reflex as rx


def blogpost_not_found() -> rx.Component:
    return rx.vstack(
        rx.heading("Blog Post Not found"),
        spacing="5",
        align="center",
        min_height="85vh",
    )
