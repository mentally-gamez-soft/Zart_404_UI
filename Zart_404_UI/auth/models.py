from datetime import datetime

import reflex as rx
import sqlalchemy
from reflex_local_auth.user import LocalUser
from sqlmodel import Field, Relationship

from Zart_404_UI.tools.utils import get_utc_now


class UserInfo(rx.Model, table=True):
    user_id: int = Field(foreign_key="localuser.id")
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
