import reflex as rx
from reflex.style import toggle_color_mode

from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.constantes.routes import URLS
from Zart_404_UI.models import UserInfo
from Zart_404_UI.routes.navigation_state import NavState


def sidebar_logout_item() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("log-out"),
            rx.text("Log Out", size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "cursor": "pointer",
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "color": rx.color("accent", 11),
                "border-radius": "0.5em",
            },
        ),
        on_click=NavState.to_logout,
        as_="button",
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_dark_mode_toggle_item() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.color_mode_cond(
                light=rx.icon("moon"),
                dark=rx.icon("sun"),
            ),
            rx.text(
                rx.color_mode_cond(
                    light="Activate Dark Mode",
                    dark="Activate Light Mode",
                ),
                size="4",
            ),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "cursor": "pointer",
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "color": rx.color("accent", 11),
                "border-radius": "0.5em",
            },
        ),
        on_click=toggle_color_mode,
        as_="button",
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_user_item(display_type: str) -> rx.Component:

    auth_user_info: UserInfo = UserSessionState.authenticated_user_info
    # label_user_name: str = rx.cond(UserSessionState.user_name,UserSessionState.user_name, "My Account")   # auth_user_info.local_user.username  # UserSessionState.authenticated_user_info[1] # rx.cond(auth_user_info & auth_user_info.local_user.username, auth_user_info.local_user.username,"My Account") # auth_user_info.local_user.username
    label_user_name: str = rx.cond(
        UserSessionState.authenticated_username,
        UserSessionState.authenticated_username,
        "My Account",
    )

    icon_button = rx.icon_button(
        rx.icon("user"),
        size="3",
        radius="full",
    )
    account_info = rx.vstack(
        rx.box(
            rx.text(
                label_user_name,
                size="3",
                weight="bold",
            ),
            rx.text(
                auth_user_info.email,
                size="2",
                weight="medium",
            ),
            width="100%",
        ),
        spacing="0",
        align="start",
        justify="start",
        width="100%",
    )

    return rx.cond(
        auth_user_info,
        rx.cond(
            display_type == "desktop",
            rx.hstack(
                icon_button,
                account_info,
                padding_x="0.5rem",
                justify="start",
                width="100%",
                align="center",
            ),
            rx.hstack(
                icon_button,
                account_info,
                padding_x="0.5rem",
                justify="start",
                width="100%",
            ),
        ),
        rx.fragment(""),
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Dashboard", "layout-dashboard", URLS["home"]),
        sidebar_item("Blog", "notebook-tabs", URLS["blogs"]),
        sidebar_item("Create Post", "notebook-pen", URLS["add_blog_post"]),
        sidebar_item("Contact", "mail", URLS["contact"]),
        # sidebar_item("Messages", "mail", "/#"),
        spacing="1",
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Reflex", size="7", weight="bold"),
                    align="center",
                    justify="start",
                    padding_x="0.5rem",
                    width="100%",
                ),
                sidebar_items(),
                rx.spacer(),
                rx.vstack(
                    rx.vstack(
                        sidebar_dark_mode_toggle_item(),
                        # sidebar_item(
                        #     "Settings", "settings", "/#"
                        # ),
                        # sidebar_item(
                        #     "Log out", "log-out", "/#"
                        # ),
                        sidebar_logout_item(),
                        spacing="1",
                        width="100%",
                    ),
                    rx.divider(),
                    # =====================================================
                    sidebar_user_item("desktop"),
                    # =============================
                    width="100%",
                    spacing="5",
                ),
                spacing="5",
                # position="fixed",
                # left="0px",
                # top="0px",
                # z_index="5",
                padding_x="1em",
                padding_y="1.5em",
                bg=rx.color("accent", 3),
                align="start",
                height="100vh",
                # height="650px",
                width="16em",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(rx.icon("align-justify", size=30)),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(rx.icon("x", size=30)),
                                width="100%",
                            ),
                            sidebar_items(),
                            rx.spacer(),
                            rx.vstack(
                                rx.vstack(
                                    sidebar_dark_mode_toggle_item(),
                                    # sidebar_item(
                                    #     "Settings",
                                    #     "settings",
                                    #     "/#",
                                    # ),
                                    # sidebar_item(
                                    #     "Log out",
                                    #     "log-out",
                                    #     "/#",
                                    # ),
                                    sidebar_logout_item(),
                                    width="100%",
                                    spacing="1",
                                ),
                                rx.divider(margin="0"),
                                # ===================================================
                                sidebar_user_item("mobile"),
                                # ============================================
                                width="100%",
                                spacing="5",
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )
