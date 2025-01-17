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


def add_entry_to_agenda_page() -> rx.Component:

    agenda_form = rx.form(
        rx.vstack(
            rx.hstack(
                rx.icon("map", size=40),
                rx.cond(
                    AgendaState.edit_mode_agenda_active,
                    autocomplete(
                        name="country",
                        placeholder="Country Location",
                        required=True,
                        width="100%",
                        state=AgendaFormState,
                        edit_mode=True,
                        value=AgendaState.edit_agenda.country,
                    ),
                    autocomplete(
                        name="country",
                        placeholder="Country Location",
                        required=True,
                        width="100%",
                        state=AgendaFormState,
                    ),
                ),
                rx.icon("map-pinned", size=40),
                # rx.cond(AgendaState.edit_mode_agenda_active,
                autocomplete_town_search(
                    town=AgendaState.edit_agenda.town
                ),  # CZO BUG ICI
                #     autocomplete_town_search(),
                # ),
                width="100%",
            ),
            rx.divider(size="4"),
            rx.hstack(
                rx.vstack(
                    rx.heading("From:", size="2"),
                    rx.input(
                        default_value=AgendaState.display_date,
                        on_change=AgendaState.handle_on_change_from_date,
                        type="date",
                        name="from_date",
                        width="100%",
                        required=True,
                    ),
                    width="100%",
                ),
                rx.vstack(
                    rx.heading("To:", size="2"),
                    rx.input(
                        # default_value=AgendaState.agenda_to_date,
                        default_value=AgendaState.display_date,
                        on_change=AgendaState.handle_on_change_to_date,
                        type="date",
                        name="to_date",
                        width="100%",
                        required=True,
                    ),
                    width="100%",
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

    return base_page(
        rx.vstack(
            rx.heading("Gestion agenda", size="9"),
            rx.desktop_only(
                rx.box(agenda_form, width="50vw"), rx.box(agenda_list_page())
            ),
            rx.mobile_and_tablet(
                rx.box(agenda_form, width="85vw"),
                rx.box(agenda_list_page()),
            ),
            spacing="5",
            align="center",
            min_height="95vh",
        ),
    )
