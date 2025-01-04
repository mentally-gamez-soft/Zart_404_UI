from datetime import datetime

import reflex as rx
import sqlalchemy
from sqlmodel import Field

from Zart_404_UI.tools import get_utc_now


class BlogPostModel(rx.Model, table=True):
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
