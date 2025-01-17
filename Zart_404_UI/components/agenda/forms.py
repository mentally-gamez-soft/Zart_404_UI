import reflex as rx

from Zart_404_UI.components.autocomplete_search_input.component import (
    autocomplete,
)
from Zart_404_UI.pages.base_page import base_page

from .agenda import agenda_list_page
from .state import AgendaFormState, AgendaState


def autocomplete_town_search(town: str = AgendaFormState.search_towns):
    return (
        rx.vstack(
            rx.input(
                required=False,
                name="town",
                placeholder="Town Location",
                value=town,
                # value=AgendaFormState.search_towns,
                on_change=AgendaFormState.set_search_towns,
                on_focus=AgendaFormState.set_search_towns_is_focused(True),
                on_blur=AgendaFormState.set_search_towns_is_focused(
                    False
                ).debounce(500),
            ),
            rx.cond(
                AgendaFormState.town_available_completions,
                rx.vstack(
                    rx.foreach(
                        AgendaFormState.town_available_completions,
                        lambda option: rx.text(
                            option,
                            on_click=AgendaFormState.set_search_towns(option),
                            size="2",
                            width="100%",
                            cursor="pointer",
                            _hover={"background_color": rx.color("accent", 4)},
                        ),
                    ),
                    width="100%",
                    background_color=rx.color("accent", 1),
                    position="absolute",
                    top="32px",
                    padding="5px",
                ),
            ),
            width="100%",
            position="relative",
        ),
    )


def form_agenda_edition():
    return rx.form(
        rx.vstack(
            rx.hstack(
                rx.icon("map", size=40),
                autocomplete(
                    name="country",
                    placeholder="Country Location",
                    required=False,
                    width="100%",
                    state=AgendaFormState,
                    value=AgendaState.edit_agenda.country,
                ),
                rx.icon("map-pinned", size=40),
                autocomplete_town_search(town=AgendaState.edit_agenda.town),
                width="100%",
            ),
            rx.divider(size="4"),
            rx.hstack(
                custom_date_input(
                    title="From:",
                    title_size=2,
                    name="from_date",
                    default_value=AgendaState.edit_from_date,
                    on_change=AgendaState.handle_on_change_from_date,
                    required=False,
                ),
                custom_date_input(
                    title="To:",
                    title_size=2,
                    name="to_date",
                    default_value=AgendaState.edit_to_date,
                    on_change=AgendaState.handle_on_change_to_date,
                    required=False,
                ),
                width="100%",
            ),
            rx.hstack(
                rx.cond(
                    AgendaState.is_valid_agenda,
                    rx.button("Submit", type="submit"),
                    rx.text(
                        "The chosen dates are already booked !",
                        color_scheme="ruby",
                    ),
                ),
                rx.button(
                    "Cancel",
                    type="submit",
                    color_scheme="ruby",
                    on_click=AgendaState.handle_cancel,
                ),
            ),
        ),
        on_submit=AgendaState.handle_submit,
        reset_on_submit=False,
    )


def form_agenda_creation():
    return rx.form(
        rx.vstack(
            rx.hstack(
                rx.icon("map", size=40),
                autocomplete(
                    name="country",
                    placeholder="Country Location",
                    required=True,
                    width="100%",
                    state=AgendaFormState,
                    value=AgendaFormState.search_text,
                ),
                rx.icon("map-pinned", size=40),
                autocomplete_town_search(),
                width="100%",
            ),
            rx.divider(size="4"),
            rx.hstack(
                custom_date_input(
                    title="From:",
                    title_size=2,
                    name="from_date",
                    default_value=AgendaState.display_date,
                    on_change=AgendaState.handle_on_change_from_date,
                    required=True,
                ),
                custom_date_input(
                    title="To:",
                    title_size=2,
                    name="to_date",
                    default_value=AgendaState.display_date,
                    on_change=AgendaState.handle_on_change_to_date,
                    required=True,
                ),
                width="100%",
            ),
            rx.cond(
                AgendaState.is_valid_agenda,
                rx.button("Submit", type="submit"),
                rx.text(
                    "The chosen dates are already booked !",
                    color_scheme="ruby",
                ),
            ),
        ),
        on_submit=AgendaState.handle_submit,
        reset_on_submit=False,
    )


def custom_date_input(
    title: str,
    title_size: int,
    name: str,
    default_value: str,
    on_change,
    input_width: str = "100%",
    required: bool = False,
    vstack_width: str = "100%",
):
    return (
        rx.vstack(
            rx.heading(title, size=f"{title_size}"),
            rx.input(
                default_value=default_value,
                on_change=on_change,
                type="date",
                name=name,
                width=input_width,
                required=required,
            ),
            width=vstack_width,
        ),
    )


def add_entry_to_agenda_page() -> rx.Component:
    agenda_creation_form = form_agenda_creation()
    agenda_edition_form = form_agenda_edition()

    return base_page(
        rx.box(
            rx.heading("My agenda", size="4"),
            rx.divider(margin_top="1em", margin_bottom="1em"),
            rx.desktop_only(
                rx.cond(
                    AgendaState.edit_mode_agenda_active,
                    rx.box(agenda_edition_form, width="50vw"),
                    rx.box(agenda_creation_form, width="50vw"),
                ),
                rx.box(agenda_list_page()),
            ),
            rx.mobile_and_tablet(
                rx.cond(
                    AgendaState.edit_mode_agenda_active,
                    rx.box(agenda_edition_form, width="85vw"),
                    rx.box(agenda_creation_form, width="85vw"),
                ),
                rx.box(agenda_list_page()),
            ),
            # spacing="5",
            align="center",
            min_height="85vh",
        ),
    )
