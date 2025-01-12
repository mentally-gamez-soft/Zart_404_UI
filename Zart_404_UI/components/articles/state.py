from datetime import datetime
from typing import List, Optional

import reflex as rx
import sqlalchemy.orm
from slugify import slugify
from sqlmodel import select

from Zart_404_UI.auth.state import UserSessionState
from Zart_404_UI.constantes import URLS
from Zart_404_UI.models import BlogPostModel, UserInfo


class ArticlePublicState(UserSessionState):
    posts: List["BlogPostModel"] = []
    post: Optional["BlogPostModel"] = None

    content: str = ""

    post_publish_active: bool = False

    limit: int = 20  # pagination on article list

    def set_limit_and_reload(self, limit: int = 5):
        self.limit = limit
        self.load_posts()
        yield

    @rx.var
    def post_id(self) -> str:
        return self.router.page.params.get("post_id", "")

    @rx.event
    def set_post_publish_active(self, value: bool):
        self.post_publish_active = value

    @rx.var
    def post_url(self) -> str:
        if not self.post:
            return f"{URLS.get("articles")}"
        return f"{URLS.get("articles")}/{self.post.slug}"

    @rx.var
    def post_slug(self) -> str:
        return self.router.page.params.get("slug") or ""

    def get_post_detail(self):
        """Retrieve one specific post."""
        lookups = (BlogPostModel.publish_active == True) & (
            BlogPostModel.slug == self.post_slug
        )

        with rx.session() as session:
            if self.post_slug == "":
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
        lookup_args = BlogPostModel.publish_active == True

        with rx.session() as session:
            self.posts = session.exec(
                select(BlogPostModel)
                .options(
                    sqlalchemy.orm.joinedload(
                        BlogPostModel.userinfo
                    ).joinedload(UserInfo.local_user)
                )
                .where(lookup_args)
                .limit(self.limit)
            ).all()

    def get_post(self, post_id: int):
        """Get a single post."""
        with rx.session() as session:
            self.post = session.exec(
                select(BlogPostModel).where(BlogPostModel.id == post_id)
            ).one_or_none()

    def to_post(self, edit_page=False):
        """Convert the post to a dictionary."""
        if not self.post:
            return rx.redirect(URLS.get("articles"))
        return rx.redirect(f"{self.post_url}")
