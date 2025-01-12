import reflex as rx

from Zart_404_UI.constantes import URLS
from Zart_404_UI.models import BlogPostModel
from Zart_404_UI.pages.base_page import base_page

from .state import ArticlePublicState


def article_card_link(
    child: rx.Component, post: BlogPostModel
) -> rx.Component:
    if post is None or post.slug is None:
        return rx.fragment("No public post found !")

    return rx.card(
        rx.link(
            rx.flex(
                # rx.avatar(src="/reflex_banner.png"),
                rx.box(
                    rx.hstack(
                        rx.heading(
                            post.title,
                        ),
                        rx.text(
                            "  (by ",
                            post.userinfo.local_user.username,
                            ")",
                            size="1",
                        ),
                    ),
                    rx.text("", size="3"),
                    rx.text("", size="3"),
                    rx.text(post.content[:30] + "...", size="3"),
                ),
                spacing="2",
            ),
            href=f"/article/{post.slug}",
        ),
        as_child=True,
    )


def article_list_item(post: BlogPostModel):
    return rx.box(
        article_card_link(
            rx.heading(post.title, size="4"),
            post,
        ),
        padding="1em",
    )


def article_public_list_component(
    columns: int = 3, spacing: int = 5, limit: int = 30
) -> rx.Component:
    return rx.grid(
        rx.foreach(ArticlePublicState.posts, article_list_item),
        columns=f"{columns}",
        spacing=f"{spacing}",
        on_mount=lambda: ArticlePublicState.set_limit_and_reload(limit),
    )


def article_public_list_page() -> rx.Component:
    posts = BlogPostModel.select()
    return base_page(
        rx.box(
            rx.heading("Published Articles", size="4"),
            rx.divider(),
            article_public_list_component(),
            min_height="85vh",
        )
    )
