from datetime import datetime
from typing import List, Optional

import reflex as rx
import sqlalchemy.orm
from slugify import slugify
from sqlmodel import select

from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.constantes import URLS
from Zart_404_UI.models import BlogPostModel, UserInfo


class BlogPostState(UserSessionState):
    posts: List["BlogPostModel"] = []
    post: Optional["BlogPostModel"] = None

    content: str = ""

    post_publish_active: bool = False

    @rx.event
    def set_post_publish_active(self, value: bool):
        self.post_publish_active = value

    @rx.var(cache=False)
    def blog_post_url(self) -> str:
        if not self.post:
            return f"{URLS.get("blogs")}"
        return f"{URLS.get("blog")}/{self.post.slug}"

    @rx.var(cache=False)
    def blog_post_edit_url(self) -> str:
        if not self.post:
            return f"{URLS.get("blogs")}"
        return f"{URLS.get("blog")}/{self.post.slug}/edit"

    @rx.var(cache=True)
    def blog_post_slug(self) -> str:
        return self.router.page.params.get("slug") or ""

    def get_post_detail(self):
        """Retrieve one specific post."""
        if self.userinfo_id is None:
            self.post = None
            return

        lookups = (BlogPostModel.userinfo_id == self.userinfo_id) & (
            BlogPostModel.slug == self.blog_post_slug
        )

        with rx.session() as session:
            if self.blog_post_slug == "":
                self.post = None
                self.content = ""
                self.post_publish_active = False
                return  # No slug, no post

            sql_statement = (
                select(BlogPostModel)
                .options(
                    sqlalchemy.orm.joinedload(
                        BlogPostModel.userinfo
                    ).joinedload(UserInfo.local_user)
                )
                .where(lookups)
            )

            self.post = session.exec(sql_statement).one_or_none()
            self.content = self.post.content if self.post else ""
            self.post_publish_active = (
                self.post.publish_active if self.post else False
            )

    def load_posts(self, *args, **kwargs):
        """Load all blog posts."""
        lookup_args = ()
        # if published_only:
        #     lookup_args = (BlogPostModel.publish_active == True)
        with rx.session() as session:
            self.posts = session.exec(
                select(BlogPostModel)
                .options(sqlalchemy.orm.joinedload(BlogPostModel.userinfo))
                .where(BlogPostModel.userinfo_id == self.userinfo_id)
            ).all()

    def create_post(self, form_data: dict):
        """Add a new blog post."""
        with rx.session() as session:
            blog_post = BlogPostModel(**form_data)
            blog_post.slug = slugify(blog_post.title)
            session.add(blog_post)
            session.commit()
            session.refresh(blog_post)  # Refresh the instance to get the id
            self.post = blog_post

    def edit_post(self, id: int, updated_data: dict):
        """Edit an existing blog post."""
        with rx.session() as session:
            post = session.exec(
                select(BlogPostModel).where(BlogPostModel.id == id)
            ).one_or_none()
            if post is None:
                return
            for k, v in updated_data.items():
                setattr(post, k, v)
            post.slug = slugify(post.title)
            session.add(post)
            session.commit()
            session.refresh(post)
            self.post = post

    def get_post(self, post_id: int):
        """Get a single post."""
        with rx.session() as session:
            self.post = session.exec(
                select(BlogPostModel).where(BlogPostModel.id == post_id)
            ).one_or_none()

    def to_blog_post(self, edit_page=False):
        """Convert the post to a dictionary."""
        if not self.post:
            return rx.redirect(URLS.get("blogs"))
        if edit_page:
            return rx.redirect(f"{self.blog_post_edit_url}")
        return rx.redirect(f"{self.blog_post_url}")


class BlogPostFormState(BlogPostState):
    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        if self.userinfo_id is not None:
            self.form_data["userinfo_id"] = self.userinfo_id
        self.create_post(form_data)
        self.form_data = {}  # Clear the form data after submission
        return self.to_blog_post(edit_page=True)


class BlogPostUpdateFormState(BlogPostState):
    form_data: dict = {}

    @rx.var(cache=True)
    def publish_display_date(self) -> str:
        if not self.post:
            return datetime.now().strftime(
                "%Y-%m-%d"
            )  # format for the day YYYY-MM-DD
        if not self.post.publish_date:
            return datetime.now().strftime(
                "%Y-%m-%d"
            )  # format for the day YYYY-MM-DD
        return self.post.publish_date.strftime("%Y-%m-%d")

    @rx.var(cache=True)
    def publish_display_time(self) -> str:
        if not self.post:
            return datetime.now().strftime("%H:%M:%S")
        if not self.post.publish_date:
            return datetime.now().strftime(
                "%H:%M:%S"
            )  # format for the time HH:MM:SS
        return self.post.publish_date.strftime("%H:%M:%S")

    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        post_id = form_data.pop("id")
        publish_date = None
        publish_time = None
        if "publish_date" in form_data:
            publish_date = form_data.pop("publish_date")
        if "publish_time" in form_data:
            publish_time = form_data.pop("publish_time")
        publish_input_string = f"{publish_date} {publish_time}"
        final_publish_date = None

        try:
            final_publish_date = datetime.strptime(
                publish_input_string, "%Y-%m-%d %H:%M:%S"
            )
        except ValueError as e:
            final_publish_date = None

        publish_status = False

        if "publish_status" in form_data:
            publish_status = form_data.pop("publish_status") == "on"

        updated_data = {**form_data}
        updated_data["publish_active"] = publish_status
        updated_data["publish_date"] = final_publish_date

        self.edit_post(post_id, updated_data)
        return self.to_blog_post()
