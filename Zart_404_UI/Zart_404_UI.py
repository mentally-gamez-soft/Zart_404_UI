"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from Zart_404_UI.auth.pages import (
    custom_login_page,
    custom_register_page,
    logout_confirm_page,
)
from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.constantes import URLS
from Zart_404_UI.pages.base_page import base_page

from . import blog, pages


class State(rx.State):
    def redirect_to_about(self):
        return rx.redirect("/about")


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
            rx.button("About Us", on_click=State.redirect_to_about),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
            id="my-element-test",
        ),
    )


app = rx.App()
app.add_page(index)
app.add_page(pages.about_page, route=URLS.get("about"))
app.add_page(pages.pricing_page, route=URLS.get("pricing"))
app.add_page(
    blog.blogpost_entries_list_page,
    route=URLS.get("blogs"),
    on_load=blog.BlogPostState.load_posts,
)
app.add_page(blog.add_blog_post_page, route=URLS.get("add_blog_post"))
app.add_page(
    blog.blog_post_detail_page,
    route=URLS.get("blog_post"),
    on_load=blog.BlogPostState.get_post_detail,
)
app.add_page(
    blog.edit_blog_post_page,
    route="/blog/[slug]/edit",
    on_load=blog.BlogPostState.get_post_detail,
)


# Routes for managing users via reflex-local-auth
# /login
# /register
import reflex_local_auth

app.add_page(
    custom_login_page,  # reflex_local_auth.pages.login_page,
    route=reflex_local_auth.routes.LOGIN_ROUTE,
    title="Login",
)
app.add_page(
    logout_confirm_page,  # reflex_local_auth.pages.login_page,
    route=URLS["logout"],
    title="Logout",
)
app.add_page(
    custom_register_page,  # reflex_local_auth.pages.register_page,
    route=reflex_local_auth.routes.REGISTER_ROUTE,
    title="Register",
)

# temporary protected page
app.add_page(
    pages.protected_page, route="/protected/", on_load=UserSessionState.on_load
)
