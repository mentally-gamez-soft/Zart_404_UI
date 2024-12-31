from datetime import datetime, timezone

import reflex as rx
import sqlalchemy
from sqlmodel import Field


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


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
