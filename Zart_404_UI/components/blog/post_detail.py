import reflex as rx

from Zart_404_UI.pages.base_page import base_page

from .state import BlogPostState


def blog_post_detail_page() -> rx.Component:
    can_edit: bool = True
    edit_link = rx.link(
        "Edit", href=f"{BlogPostState.blog_post_edit_url}"
    )  # style="btn btn-primary")
    edit_link_element = rx.cond(can_edit, edit_link, rx.fragment(""))
    return base_page(
        rx.vstack(
            rx.hstack(
                rx.heading(BlogPostState.post.title, size="9"),
                edit_link_element,
                align="end",
            ),
            rx.text(BlogPostState.post.publish_date),
            rx.text(
                BlogPostState.post.content,
                white_space="pre-wrap",
            ),
            spacing="5",
            min_height="85vh",
            id="about-page",
        ),
    )
