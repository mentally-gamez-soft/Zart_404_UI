import reflex as rx


def get_icon_trash(padding: str = "2px") -> rx.Component:
    return rx.icon(tag="trash-2", padding=padding)


def get_icon_edit(padding: str = "2px") -> rx.Component:
    return rx.icon(tag="pencil", padding=padding)


def get_icon(action: str, padding: str = "2px") -> rx.Component:
    return rx.match(
        action,
        ("Delete", get_icon_trash(padding=padding)),
        ("Modify", get_icon_edit(padding=padding)),
        rx.text("Unknown action."),
    )
