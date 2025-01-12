import reflex as rx

from Zart_404_UI.pages.base_page import base_page

from .agenda import agenda_list_page
from .state import AgendaState


def add_entry_to_agenda_page() -> rx.Component:

    agenda_form = rx.form(
        rx.vstack(
            rx.hstack(
                rx.icon("map"),
                rx.input(
                    name="country",
                    placeholder="Country Location",
                    required=True,
                    width="100%",
                ),
                rx.icon("map-pinned"),
                rx.input(
                    name="town",
                    placeholder="Town Location",
                    required=False,
                    width="100%",
                ),
                width="100%",
            ),
            rx.hstack(
                rx.input(
                    default_value=AgendaState.display_date,
                    type="date",
                    name="from_date",
                    width="100%",
                    required=True,
                ),
                rx.input(
                    default_value=AgendaState.display_date,
                    type="date",
                    name="to_date",
                    width="100%",
                    required=True,
                ),
                width="100%",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=AgendaState.handle_submit,
        reset_on_submit=False,
    )

    return base_page(
        rx.vstack(
            rx.heading("Gestion agenda", size="9"),
            rx.desktop_only(
                rx.box(agenda_form, width="50vw"), rx.box(agenda_list_page())
            ),
            rx.mobile_and_tablet(agenda_form, width="85vw"),
            spacing="5",
            align="center",
            min_height="95vh",
        ),
    )
