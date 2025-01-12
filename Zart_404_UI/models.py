from datetime import datetime
from typing import List, Optional

import reflex as rx
import sqlalchemy
from reflex_local_auth.user import LocalUser
from sqlmodel import Field, Relationship

from Zart_404_UI.tools.utils import get_utc_now


class UserInfo(rx.Model, table=True):
    user_id: int = Field(foreign_key="localuser.id", ondelete="CASCADE")
    local_user: LocalUser | None = Relationship()

    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )

    email: str
    created_from_ip: str

    # relationship one to many user <====> blogs + contact entries
    posts: List["BlogPostModel"] = Relationship(
        cascade_delete=True, back_populates="userinfo"
    )
    contact_entries: List["ContactEntryModel"] = Relationship(
        cascade_delete=True, back_populates="userinfo"
    )

    # A user is managing is provided a calendar
    calendar: List["AgendaModel"] = Relationship(
        cascade_delete=True, back_populates="userinfo"
    )


class BlogPostModel(rx.Model, table=True):
    # relation one to many user <===>  Blogs
    userinfo_id: int = Field(
        default=None, foreign_key="userinfo.id", ondelete="CASCADE"
    )
    userinfo: Optional["UserInfo"] = Relationship(back_populates="posts")

    title: str = Field(nullable=False)

    content: str = Field(nullable=False)

    slug: str = Field(nullable=False)

    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )

    publish_active: bool = Field(default=False)

    publish_date: datetime = Field(
        default_factory=None,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={},
        nullable=True,
    )


class ContactEntryModel(rx.Model, table=True):
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field(nullable=False)
    message: str = Field(nullable=False)
    created_datetime: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )

    # Relation one to many user <====> contact entries
    userinfo_id: int = Field(
        default=None, foreign_key="userinfo.id", ondelete="CASCADE"
    )
    userinfo: Optional["UserInfo"] = Relationship(
        back_populates="contact_entries"
    )


# Ajout de modele pour la gestion de l'agenda
class AgendaModel(rx.Model, table=True):
    userinfo_id: int = Field(
        default=None, foreign_key="userinfo.id", ondelete="CASCADE"
    )
    userinfo: Optional["UserInfo"] = Relationship(back_populates="calendar")

    country: str = Field(nullable=False)
    town: str = Field(nullable=True)

    from_date: datetime = Field(
        default_factory=None,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={},
        nullable=False,
    )

    to_date: datetime = Field(
        default_factory=None,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={},
        nullable=False,
    )
