import reflex as rx

from Zart_404_UI.components.blog.not_found_404 import blogpost_not_found
from Zart_404_UI.pages.base_page import base_page

from .state import ArticlePublicState


def article_detail_page() -> rx.Component:

    child_element = rx.cond(
        ArticlePublicState.post,
        rx.vstack(
            rx.hstack(
                rx.heading(ArticlePublicState.post.title, size="9"),
                align="end",
            ),
            rx.badge(
                rx.text(
                    "By ", ArticlePublicState.post.userinfo.local_user.username
                )
            ),
            rx.text(ArticlePublicState.post.publish_date),
            rx.text(
                ArticlePublicState.post.content,
                white_space="pre-wrap",
            ),
            spacing="5",
            min_height="85vh",
            align="center",
        ),
        blogpost_not_found(),
    )

    return base_page(child_element)
