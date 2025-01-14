import reflex as rx

from Zart_404_UI.components.speed_dials import render_speed_dial_component
from Zart_404_UI.models import AgendaModel
from Zart_404_UI.pages.base_page import base_page

from .state import AgendaState

# def speed_dial_component(index:int):
#         def menu_item(icon: str, text: str) -> rx.Component:
#             return rx.tooltip(
#                 rx.icon_button(
#                     rx.icon(icon, padding="2px"),
#                     variant="soft",
#                     color_scheme="gray",
#                     size="2",
#                     cursor="pointer",
#                     radius="full",
#                     on_click=AgendaState.handle_click_speed_dial(index,text),
#                 ),
#                 side="top",
#                 content=text,
#             )

#         def menu() -> rx.Component:
#             return rx.hstack(
#                 menu_item("pencil", "Modify"),
#                 menu_item("trash-2", "Delete"),
#                 position="absolute",
#                 bottom="0",
#                 spacing="2",
#                 padding_right="10px",
#                 right="100%",
#                 direction="row-reverse",
#                 align_items="center",
#             )

#         return rx.box(
#             rx.box(
#                 rx.icon_button(
#                     rx.icon(
#                         "plus",
#                         style={
#                             "transform": rx.cond(
#                                 SpeedDialHorizontal.f_is_open,
#                                 "rotate(45deg)",
#                                 "rotate(0)",
#                             ),
#                             "transition": "transform 150ms cubic-bezier(0.4, 0, 0.2, 1)",
#                         },
#                         class_name="dial",
#                         id=f"id-for-speed-dial-{index}",
#                     ),
#                     variant="solid",
#                     # color_scheme="jade",
#                     size="2",
#                     cursor="pointer",
#                     radius="full",
#                     position="relative",
#                 ),
#                 rx.cond(
#                     SpeedDialHorizontal.f_is_open,
#                     menu(),
#                 ),
#                 position="relative",
#             ),
#             on_mouse_enter=SpeedDialHorizontal.toggle(True),
#             on_mouse_leave=SpeedDialHorizontal.toggle(False),
#             on_click=SpeedDialHorizontal.toggle(~SpeedDialHorizontal.f_is_open),
#             style={"bottom": "7px", "right": "7px"},
#             position="absolute",
#             # z_index="50",
#             # **props,
#         )

# def render_speed_dial_component(index:int) -> rx.Component:
#     return rx.box(
#         speed_dial_component(index),
#         height="30px",
#         position="relative",
#         width="100%",
#     )


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
            rx.text(
                "", size="1"
            ),  # rx.heading("From ", agenda.from_date," TWO ", agenda.to_date, size="5"),
            agenda,
            index,
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
