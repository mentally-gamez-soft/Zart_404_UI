import reflex as rx

from .state import AgendaState


def agenda_list_item(agenda: tuple) -> rx.Component:
    country = (agenda[0][0],)
    town = (agenda[0][1],)
    start_date = agenda[1][0]
    end_date = agenda[1][1]
    return rx.vstack(
        rx.text("Country: ", country),
        rx.text("Town: ", town),
        rx.text("From: ", start_date),
        rx.text("to: ", end_date),
    )


def agenda_list_page() -> rx.Component:
    agenda = AgendaState.agenda

    return rx.vstack(
        rx.heading("Agenda", size="3"),
        rx.foreach(agenda, agenda_list_item),
        spacing="5",
        align="center",
        min_height="85vh",
    )
