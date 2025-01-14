import reflex as rx

from Zart_404_UI.models import AgendaModel
from Zart_404_UI.pages.base_page import base_page

from .state import AgendaState, SpeedDialHorizontal


def render_speed_dial() -> rx.Component:
    speed_dial_horizontal = SpeedDialHorizontal.create
    return rx.box(
        speed_dial_horizontal(),
        height="250px",
        position="relative",
        width="100%",
    )


def agenda_card(child: rx.Component, agenda: AgendaModel) -> rx.Component:

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
                render_speed_dial(),
            ),
            spacing="2",
        ),
        as_child=True,
    )


def agenda_list_item(agenda: AgendaModel):
    return rx.box(
        agenda_card(
            rx.text(
                "", size="1"
            ),  # rx.heading("From ", agenda.from_date," TWO ", agenda.to_date, size="5"),
            agenda,
        ),
        padding="1em",
    )


def calendar_list_component(
    columns: int = 3, spacing: int = 5, limit: int = 30
) -> rx.Component:
    return rx.grid(
        rx.foreach(AgendaState.calendar, agenda_list_item),
        columns=f"{columns}",
        spacing=f"{spacing}",
        on_mount=lambda: AgendaState.set_limit_and_reload(limit),
    )


def agenda_list_page() -> rx.Component:
    agenda = AgendaState.agenda

    return rx.vstack(
        rx.heading("My Calendar", size="4"),
        rx.divider(),
        calendar_list_component(columns=2, spacing=1, limit=10),
        min_height="85vh",
        spacing="5",
        align="center",
    )
