import reflex as rx
import reflex_local_auth

from Zart_404_UI.components.speed_dials import render_speed_dial_component
from Zart_404_UI.models import AgendaModel
from Zart_404_UI.pages.base_page import base_page

from .state import AgendaState


def agenda_card(
    child: rx.Component, agenda: AgendaModel, index: int
) -> rx.Component:

    return rx.card(
        rx.flex(
            # rx.avatar(src="/reflex_banner.png"),
            rx.box(
                rx.hstack(
                    rx.heading(
                        "From: ",
                        agenda.from_date,
                        size="2",
                    ),
                    rx.heading(
                        "To: ",
                        agenda.to_date,
                        size="2",
                    ),
                ),
                rx.divider(),
                # rx.text("", size="3"),
                # rx.text("", size="3"),
                rx.text(
                    agenda.country,
                    " (",
                    agenda.town,
                    ")",
                    size="2",
                ),
                # rx.divider(size="1"),
                # rx.cond(
                # ),
                render_speed_dial_component(index),
            ),
            spacing="2",
        ),
        as_child=True,
    )


def agenda_list_item(agenda: AgendaModel, index: int):
    return rx.box(
        agenda_card(
            rx.text("", size="1"),
            agenda,
            index,  # agenda.id
        ),
        padding="1em",
    )


def calendar_list_component(
    columns: int = 3, spacing: int = 5, limit: int = 30
) -> rx.Component:
    return rx.grid(
        rx.foreach(
            AgendaState.calendar,
            lambda agenda, index: agenda_list_item(agenda, index),
        ),
        columns=f"{columns}",
        spacing=f"{spacing}",
        on_mount=lambda: AgendaState.set_limit_and_reload(limit),
    )


@reflex_local_auth.require_login
def agenda_list_page() -> rx.Component:
    return rx.vstack(
        rx.heading("My Calendar", size="4"),
        rx.divider(),
        calendar_list_component(columns=2, spacing=1, limit=10),
        min_height="85vh",
        spacing="5",
        align="center",
    )
