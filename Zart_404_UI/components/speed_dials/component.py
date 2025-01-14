import reflex as rx

from .state import SpeedDialState


def speed_dial_component(index: int):
    def menu_item(icon: str, text: str) -> rx.Component:
        return rx.tooltip(
            rx.icon_button(
                rx.icon(icon, padding="2px"),
                variant="soft",
                color_scheme="gray",
                size="2",
                cursor="pointer",
                radius="full",
                on_click=SpeedDialState.handle_click_speed_dial(
                    {"index": index, "action": text}
                ),
            ),
            side="top",
            content=text,
        )

    def menu() -> rx.Component:
        return rx.hstack(
            rx.foreach(
                SpeedDialState.items,
                lambda icon_name, action: menu_item(icon_name, action),
            ),
            # menu_item("pencil", "Modify"),
            # menu_item("trash-2", "Delete"),
            position="absolute",
            bottom="0",
            spacing="2",
            padding_right="10px",
            right="100%",
            direction="row-reverse",
            align_items="center",
        )

    return rx.box(
        rx.box(
            rx.icon_button(
                rx.icon(
                    "plus",
                    style={
                        "transform": rx.cond(
                            SpeedDialState.is_open,
                            "rotate(45deg)",
                            "rotate(0)",
                        ),
                        "transition": "transform 150ms cubic-bezier(0.4, 0, 0.2, 1)",
                    },
                    class_name="dial",
                    id=f"id-for-speed-dial-{index}",
                ),
                variant="solid",
                # color_scheme="jade",
                size="2",
                cursor="pointer",
                radius="full",
                position="relative",
            ),
            rx.cond(
                SpeedDialState.is_open,
                menu(),
            ),
            position="relative",
        ),
        on_mouse_enter=SpeedDialState.toggle(True),
        on_mouse_leave=SpeedDialState.toggle(False),
        on_click=SpeedDialState.toggle(~SpeedDialState.f_is_open),
        style={"bottom": "7px", "right": "7px"},
        position="absolute",
        # z_index="50",
        # **props,
    )


def render_speed_dial_component(index: int) -> rx.Component:
    return rx.box(
        # rx.foreach(SpeedDialState.items,lambda icon_name,action: speed_dial_component(index, icon_name, action)),
        speed_dial_component(index),
        height="30px",
        position="relative",
        width="100%",
    )
