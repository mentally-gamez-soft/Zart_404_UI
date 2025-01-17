import reflex as rx


def autocomplete(
    name: str,
    placeholder: str,
    state: rx.State,
    value: str,
    required: bool = False,
    width: str = "100%",
):
    return (
        rx.vstack(
            rx.input(
                required=required,
                name=name,
                placeholder=placeholder,
                value=value,
                on_change=state.set_search_text,
                on_focus=state.set_search_is_focused(True),
                on_blur=state.handle_custom_on_blur(False).debounce(500),
            ),
            rx.cond(
                state.default_available_completions,
                rx.vstack(
                    rx.foreach(
                        state.default_available_completions,
                        lambda option: rx.text(
                            option,
                            on_click=state.set_search_text(option),
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
            width=width,
            position="relative",
        ),
    )
