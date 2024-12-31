import reflex as rx

from Zart_404_UI.constantes import heading, logo

NAVBAR_TITLE = "Zart-404"
LOGIN_BUTTON_MESSAGE = "Log In"
SIGNUP_BUTTON_MESSAGE = "Sign Up"


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(rx.text(text, size="4", weight="medium"), href=url)


def navbar_links(media_type: str) -> list:
    if media_type == "desktop":
        return [
            navbar_link("Home", "/#"),
            navbar_link("About", "/#"),
            navbar_link("Pricing", "/#"),
            navbar_link("Contact", "/#"),
        ]
    return [
        rx.menu.item("Home"),
        rx.menu.item("About"),
        rx.menu.item("Pricing"),
        rx.menu.item("Contact"),
    ]


def navbar_logo(media_type: str) -> rx.Component:
    if media_type == "desktop":
        return rx.image(
            src=logo["img-src"],
            width=logo["desktop-layout"]["width"],
            height=logo["desktop-layout"]["height"],
            border_radius=logo["desktop-layout"]["border_radius"],
        )

    return rx.image(
        src=logo["img-src"],
        width=logo["mobile-layout"]["width"],
        height=logo["mobile-layout"]["height"],
        border_radius=logo["mobile-layout"]["border_radius"],
    )


def navbar_title(media_type: str, title: str) -> rx.Component:
    if media_type == "desktop":
        return rx.heading(
            title,
            size=heading["desktop-layout"]["size"],
            weight=heading["desktop-layout"]["weight"],
        )

    return rx.heading(
        title,
        size=heading["mobile-layout"]["size"],
        weight=heading["mobile-layout"]["weight"],
    )


def navbar(title: str) -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    navbar_logo("desktop"),
                    navbar_title(media_type="desktop", title=title),
                    align_items="center",
                ),
                rx.hstack(
                    *navbar_links(media_type="desktop"),
                    spacing="5",
                ),
                rx.hstack(
                    rx.button(
                        SIGNUP_BUTTON_MESSAGE,
                        size="3",
                        variant="outline",
                    ),
                    rx.button(LOGIN_BUTTON_MESSAGE, size="3"),
                    spacing="4",
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    navbar_logo("mobile"),
                    navbar_title(media_type="mobile", title=title),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        *navbar_links(media_type="mobile"),
                        rx.menu.separator(),
                        rx.menu.item(LOGIN_BUTTON_MESSAGE),
                        rx.menu.item(SIGNUP_BUTTON_MESSAGE),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
        id="navbar-id",
    )
