import reflex as rx

from Zart_404_UI.pages.base_page import base_page

from .state import BlogPostFormState, BlogPostUpdateFormState


def add_blog_post_page() -> rx.Component:
    blog_post_form = rx.form(
        rx.vstack(
            rx.hstack(
                rx.input(
                    name="title",
                    placeholder="Title",
                    required=True,
                    width="100%",
                ),
                width="100%",
            ),
            rx.text_area(
                name="content",
                placeholder="Your post here",
                required=True,
                height="50vh",
                width="100%",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=BlogPostFormState.handle_submit,
        reset_on_submit=True,
    )

    return base_page(
        rx.vstack(
            rx.heading("New blog post", size="9"),
            rx.desktop_only(rx.box(blog_post_form, width="50vw")),
            rx.mobile_and_tablet(blog_post_form, width="85vw"),
            spacing="5",
            align="center",
            min_height="95vh",
        ),
    )


def edit_blog_post_page() -> rx.Component:
    post = BlogPostUpdateFormState.post
    content = post.content if post is not None else ""
    title = post.title if post is not None else ""
    publish_active = post.publish_active if post is not None else False

    blog_post_form = rx.form(
        rx.box(
            rx.input(name="id", type="hidden", value=post.id), display="none"
        ),
        rx.vstack(
            rx.hstack(
                rx.input(
                    default_value=title,
                    name="title",
                    placeholder="Title",
                    required=True,
                    width="100%",
                ),
                width="100%",
            ),
            rx.text_area(
                name="content",
                placeholder="Your post here",
                required=True,
                height="50vh",
                width="100%",
                value=content,
                on_change=BlogPostUpdateFormState.set_content,
            ),
            rx.flex(
                rx.switch(
                    default_checked=BlogPostUpdateFormState.post_publish_active,
                    on_change=BlogPostUpdateFormState.set_post_publish_active,
                    name="publish_status",
                ),
                rx.text("Publish Status"),
                spacing="2",
                # id="my-switch-here",
            ),
            rx.cond(
                BlogPostUpdateFormState.post_publish_active,
                rx.hstack(
                    rx.input(
                        default_value=BlogPostUpdateFormState.publish_display_date,
                        type="date",
                        name="publish_date",
                        width="100%",
                    ),
                    rx.input(
                        default_value=BlogPostUpdateFormState.publish_display_time,
                        type="time",
                        name="publish_time",
                        width="100%",
                    ),
                    width="100%",
                ),
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=BlogPostUpdateFormState.handle_submit,
    )

    return base_page(
        rx.vstack(
            rx.heading("Editing post: ", post.title, size="9"),
            rx.desktop_only(rx.box(blog_post_form, width="50vw")),
            rx.mobile_and_tablet(blog_post_form, width="85vw"),
            spacing="5",
            align="center",
            min_height="95vh",
        ),
    )
