import reflex as rx
import reflex_local_auth

from Zart_404_UI.constantes import URLS
from Zart_404_UI.models import BlogPostModel
from Zart_404_UI.pages.base_page import base_page

from .state import BlogPostState as state


def blog_post_detail_link(
    child: rx.Component, post: BlogPostModel
) -> rx.Component:
    if post is None or post.id is None:
        return rx.fragment(child)

    return rx.link(
        child,
        rx.heading("By ", post.userinfo.email, size="4"),
        href=f"/blog/{post.slug}",
    )


def blog_post_list_item(post: BlogPostModel) -> rx.Component:
    return rx.box(
        blog_post_detail_link(
            rx.heading(post.title, size="4"),
            post,
        ),
        padding="1em",
    )


@reflex_local_auth.require_login
def blogpost_entries_list_page() -> rx.Component:
    posts = BlogPostModel.select()
    return base_page(
        rx.vstack(
            rx.heading("Blog Posts", size="3"),
            rx.link(
                rx.button("Add Blog Post"),
                href=f"/{URLS.get("add_blog_post")}",
            ),
            rx.foreach(state.posts, blog_post_list_item),
            spacing="5",
            align="center",
            min_height="85vh",
        )
    )
